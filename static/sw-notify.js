// Service Worker for ChaiTalks.Tech notifications
// Checks for new content via the site's JSON index

const CACHE_KEY = 'chaitalks-last-check';
const CHECK_INTERVAL = 60 * 60 * 1000; // 1 hour

self.addEventListener('install', function(event) {
  self.skipWaiting();
});

self.addEventListener('activate', function(event) {
  event.waitUntil(self.clients.claim());
});

// Periodic check triggered by main thread messages
self.addEventListener('message', function(event) {
  if (event.data && event.data.type === 'CHECK_NEW_CONTENT') {
    checkForNewContent();
  }
});

async function checkForNewContent() {
  try {
    const response = await fetch('/index.json?_=' + Date.now());
    if (!response.ok) return;

    const posts = await response.json();
    if (!posts || posts.length === 0) return;

    // Get stored state
    const cache = await caches.open('chaitalks-notifications');
    const storedResponse = await cache.match(CACHE_KEY);
    let storedData = { knownUrls: [], lastCheck: 0 };

    if (storedResponse) {
      storedData = await storedResponse.json();
    }

    const knownUrls = new Set(storedData.knownUrls || []);
    const currentUrls = posts.map(function(p) { return p.permalink; });

    // Find new posts (not in our known set)
    const newPosts = [];
    for (var i = 0; i < posts.length; i++) {
      if (!knownUrls.has(posts[i].permalink)) {
        newPosts.push(posts[i]);
      }
    }

    // Only notify if we had a previous check (not first visit)
    if (storedData.knownUrls.length > 0 && newPosts.length > 0) {
      for (var j = 0; j < Math.min(newPosts.length, 3); j++) {
        self.registration.showNotification('ChaiTalks.Tech', {
          body: newPosts[j].title,
          icon: '/logo.png',
          badge: '/logo.png',
          tag: 'new-post-' + newPosts[j].permalink,
          data: { url: newPosts[j].permalink }
        });
      }

      if (newPosts.length > 3) {
        self.registration.showNotification('ChaiTalks.Tech', {
          body: 'And ' + (newPosts.length - 3) + ' more new posts!',
          icon: '/logo.png',
          badge: '/logo.png',
          tag: 'new-posts-more',
          data: { url: '/' }
        });
      }
    }

    // Store current state
    await cache.put(CACHE_KEY, new Response(JSON.stringify({
      knownUrls: currentUrls,
      lastCheck: Date.now()
    })));
  } catch (e) {
    // Silently fail - notifications are best-effort
  }
}

// Handle notification click - open the post
self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  var url = event.notification.data && event.notification.data.url ? event.notification.data.url : '/';
  event.waitUntil(
    self.clients.matchAll({ type: 'window' }).then(function(clientList) {
      for (var i = 0; i < clientList.length; i++) {
        if (clientList[i].url === url && 'focus' in clientList[i]) {
          return clientList[i].focus();
        }
      }
      if (self.clients.openWindow) {
        return self.clients.openWindow(url);
      }
    })
  );
});
