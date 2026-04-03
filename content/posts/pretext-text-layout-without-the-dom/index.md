---
title: "Pretext: Measuring Text Without Touching the DOM"
date: 2026-04-03
draft: false
categories:
  - "javascript"
  - "developer-tools"
tags:
  - "canvas"
  - "javascript"
  - "layout"
  - "performance"
  - "text-rendering"
  - "typescript"
  - "virtual-scroll"
  - "web-performance"
description: "Pretext is a small library that measures paragraph heights and handles text layout without triggering DOM reflow. Here is how it works and why it matters."
---

Here is a problem you have probably run into. You need to know how tall a block of text is before it renders. Maybe you are building a virtual scroll list and need to allocate space for off-screen items. Maybe you are laying out a chat UI and want the window to land at the right scroll position before messages appear. So you do the thing everyone does: insert the element into the DOM with `visibility: hidden`, read `offsetHeight`, then pull it back out.

It works. But it forces the browser to do a full layout calculation every single time you do it. Do that for 500 messages and you feel it.

**[Pretext](https://github.com/chenglou/pretext)** is a small TypeScript library by Cheng Lou that takes a different approach entirely. Cheng Lou has serious frontend chops — he worked on React's reconciler, built ReasonML, and more recently worked at Midjourney. Pretext feels like something that came out of staring at real rendering bottlenecks for a long time.

* * *

## What It Does Differently

Instead of touching the DOM at all, Pretext uses the Canvas 2D API. Specifically, it calls `ctx.measureText()` on an offscreen canvas with font settings that match your actual CSS.

The key thing here: the browser uses the same underlying font engine for both canvas rendering and DOM layout. So the measurements you get back are accurate. And critically, `ctx.measureText()` does not trigger a reflow. It is a pure computation. You can call it thousands of times in a row without the browser recalculating a single layout tree.

That is the whole insight. It sounds almost too simple when you say it out loud.

* * *

## Two Functions, Two Jobs

The API is split into two phases, and that split is intentional.

`prepare()` is the setup phase. You call it once when your content loads (or when your font stack changes). It does the upfront work of computing font metrics and running the line-breaking logic for each text block. For 500 texts, this takes around 19ms. You pay that cost once.

`layout()` is the fast path. Once `prepare()` has done its thing, `layout()` recalculates paragraph heights for a given container width. This is what you call on every resize event, or whenever you need to reflow. The same 500 texts take about 0.09ms. That is roughly 200 times faster than measuring through the DOM.

The reason the split works is that most of the expensive work is in the font metrics and line-breaking, which stays stable as long as your content and font settings don't change. Layout recalculation on resize is mostly geometry, which is cheap once you have the metrics cached.

```js
import { prepare, layout } from 'pretext';

// Run once when content loads
const prepared = await prepare(texts, { font: '16px Inter, sans-serif', width: 600 });

// Run on every resize
const heights = layout(prepared, containerWidth);
```

* * *

## See It in Action

The official demo site shows several different use cases — editorial columns, fluid text simulation, and a chat UI — all running at 60fps with no layout reflow:

{{< iframe src="https://chenglou.me/pretext/" height="520" title="Pretext live demo" >}}

If the embed above does not load in your browser, head directly to [chenglou.me/pretext](https://chenglou.me/pretext/) to see it running.

* * *

## Where This Actually Helps

Chat UIs are the obvious one. You need bubble heights before messages appear so the scroll position lands correctly. Without something like Pretext, you are either guessing (and getting layout shift) or measuring through the DOM (and taking the reflow hit).

Virtual scroll is another strong fit. Windowed list libraries need to estimate item heights for items that are not currently rendered. Most of them either assume a fixed height or use an average-based heuristic. With Pretext, you can get actual heights for all your items upfront.

Masonry and editorial grid layouts also benefit. When you are assigning items to columns based on height, you need those heights before you place anything. The usual approach is to render everything, measure, then reposition — which causes a visible flash. Pretext lets you skip the first render entirely.

And then there is the case where there is no DOM at all: worker threads, server-side layout calculations, or any context where you want to compute layout without a browser environment. Canvas measurement works in workers, DOM measurement does not.

* * *

## The Caveats

A few things worth knowing before you reach for it.

Pretext measures plain text runs. If your content has complex inline HTML — links inside paragraphs, inline images, mixed font weights mid-sentence — you will need to think carefully about how to break that up. It handles multilingual text and emoji well, but the more your layout diverges from a simple paragraph, the more work you need to do on the integration side.

Font loading matters a lot. If you call `prepare()` before your custom fonts have finished loading, the measurements will use fallback font metrics and will be wrong. The fix is to wait for `document.fonts.ready` before calling `prepare()`. This is easy to forget.

It is also a relatively young library. The API has settled down, but if you are building something that needs long-term stability, keep an eye on the [GitHub repo](https://github.com/chenglou/pretext) for changes.

* * *

Using the DOM to measure text has always been a bit of a workaround. The DOM was designed to render content, not to act as a measurement oracle, and the reflow cost is just the price you pay for abusing it that way. Pretext is one of those tools that makes you wonder why it took this long to exist.

It fits into a broader shift happening in frontend work right now: moving more computation out of the browser's main layout pipeline. Virtual scroll, `ResizeObserver`, off-thread rendering in workers — all of it points in the same direction. Pretext is a small but well-aimed piece of that puzzle.

Worth a look at the [repo](https://github.com/chenglou/pretext) if any of this sounds like your problem.
