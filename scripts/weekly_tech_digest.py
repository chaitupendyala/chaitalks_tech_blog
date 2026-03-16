#!/usr/bin/env python3
"""Weekly Tech Digest Generator.

Fetches top stories from Hacker News, uses OpenAI to summarize and rank them,
and generates a Hugo blog post for the weekly tech digest.
"""

import json
import sys
import time
import datetime
import pathlib

import requests
import openai

# Paths
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content" / "posts"

# Hacker News API
HN_API = "https://hacker-news.firebaseio.com/v0"
TOP_N_FETCH = 50
REQUEST_DELAY = 0.05  # 50ms between HN API calls

# OpenAI
OPENAI_MODEL = "gpt-4o"


def fetch_top_story_ids():
    """Fetch the list of top story IDs from Hacker News."""
    resp = requests.get(f"{HN_API}/topstories.json", timeout=15)
    resp.raise_for_status()
    return resp.json()


def fetch_item(item_id):
    """Fetch a single item from Hacker News by ID."""
    resp = requests.get(f"{HN_API}/item/{item_id}.json", timeout=15)
    resp.raise_for_status()
    time.sleep(REQUEST_DELAY)
    return resp.json()


def get_recent_top_stories(n=TOP_N_FETCH):
    """Fetch top HN stories from the past 7 days, sorted by score."""
    story_ids = fetch_top_story_ids()
    cutoff = time.time() - 7 * 86400  # 7 days ago

    stories = []
    for story_id in story_ids:
        if len(stories) >= n:
            break

        try:
            item = fetch_item(story_id)
        except (requests.RequestException, json.JSONDecodeError):
            continue

        if item is None:
            continue
        if item.get("type") != "story":
            continue
        if item.get("time", 0) < cutoff:
            continue
        if not item.get("url"):
            continue

        stories.append({
            "title": item.get("title", "Untitled"),
            "url": item["url"],
            "score": item.get("score", 0),
            "comments": item.get("descendants", 0),
            "author": item.get("by", "unknown"),
            "hn_url": f"https://news.ycombinator.com/item?id={item['id']}",
        })

    stories.sort(key=lambda s: s["score"], reverse=True)
    return stories


def generate_digest(stories, digest_date):
    """Use OpenAI to summarize and rank the top stories."""
    stories_text = "\n".join(
        f"{i+1}. \"{s['title']}\" — {s['url']} (Score: {s['score']}, "
        f"Comments: {s['comments']})"
        for i, s in enumerate(stories)
    )

    system_prompt = """You are a tech journalist writing a weekly digest for a developer blog.
You will receive a list of top Hacker News stories from the past week.

Your task:
1. Select the 10 most significant and interesting stories.
2. Group them into 3-5 thematic categories (e.g., "AI and Machine Learning",
   "Programming and Developer Tools", "Security", "Open Source", "Industry News").
3. For each story, write a 2-3 sentence summary explaining what happened and why it matters.
4. Write a 2-3 sentence intro paragraph for the weekly digest.
5. Suggest relevant tags (lowercase, hyphenated, e.g. "machine-learning").

Return your response as a JSON object with this exact schema:
{
  "intro": "string",
  "categories": [
    {
      "name": "Category Name",
      "stories": [
        {
          "title": "string",
          "url": "string",
          "hn_url": "string",
          "summary": "string",
          "score": 123,
          "comments": 45
        }
      ]
    }
  ],
  "tags": ["tag1", "tag2"]
}"""

    user_prompt = (
        f"Here are the top Hacker News stories from the week ending "
        f"{digest_date.strftime('%B %d, %Y')}:\n\n{stories_text}\n\n"
        f"Here is the mapping of story titles to HN discussion URLs:\n"
    )
    for s in stories:
        user_prompt += f"- \"{s['title']}\" → {s['hn_url']}\n"

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0.7,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return json.loads(response.choices[0].message.content)


def render_markdown(digest_data, digest_date):
    """Render the digest data as a Hugo-compatible markdown post."""
    date_str = digest_date.strftime("%Y-%m-%d")
    title = f"Weekly Tech Digest - {digest_date.strftime('%B %d, %Y')}"

    # Build tags list
    base_tags = ["weekly-digest", "tech-news", "hacker-news"]
    extra_tags = digest_data.get("tags", [])
    all_tags = sorted(set(base_tags + extra_tags))

    # Frontmatter
    tags_yaml = "\n".join(f'  - "{t}"' for t in all_tags)
    frontmatter = f"""---
title: "{title}"
date: {date_str}
description: "This week's top tech stories from Hacker News, curated and summarized"
tags:
{tags_yaml}
categories:
  - "tech-news"
---"""

    # Body
    body_parts = [digest_data.get("intro", "")]

    for category in digest_data.get("categories", []):
        body_parts.append(f"\n## {category['name']}\n")
        for story in category.get("stories", []):
            body_parts.append(f"### {story['title']}\n")
            body_parts.append(f"{story['summary']}\n")
            score = story.get("score", "")
            comments = story.get("comments", "")
            meta_parts = []
            if score:
                meta_parts.append(f"{score} points")
            if comments:
                meta_parts.append(f"{comments} comments")
            meta = " | ".join(meta_parts)
            body_parts.append(
                f"[Read the article]({story['url']}) · "
                f"[HN Discussion]({story['hn_url']})"
                + (f" ({meta})" if meta else "")
                + "\n"
            )

    return frontmatter + "\n\n" + "\n".join(body_parts)


def write_post(markdown_content, digest_date):
    """Write the markdown post to the content directory."""
    slug = f"weekly-tech-digest-{digest_date.strftime('%Y-%m-%d')}"
    post_dir = CONTENT_DIR / slug
    post_dir.mkdir(parents=True, exist_ok=True)
    post_file = post_dir / "index.md"
    post_file.write_text(markdown_content, encoding="utf-8")
    return post_file


def main():
    digest_date = datetime.date.today()

    print("Fetching top HN stories from the past week...")
    try:
        stories = get_recent_top_stories()
    except requests.RequestException as e:
        print(f"Error fetching from Hacker News: {e}", file=sys.stderr)
        sys.exit(1)

    if not stories:
        print("No stories found from the past week. Exiting.")
        sys.exit(0)

    print(f"Found {len(stories)} stories. Sending to OpenAI for summarization...")
    try:
        digest_data = generate_digest(stories, digest_date)
    except (openai.OpenAIError, json.JSONDecodeError, KeyError) as e:
        print(f"Error generating digest: {e}", file=sys.stderr)
        sys.exit(1)

    print("Generating markdown post...")
    markdown = render_markdown(digest_data, digest_date)

    print("Writing post file...")
    output_path = write_post(markdown, digest_date)
    print(f"Post written to: {output_path}")


if __name__ == "__main__":
    main()
