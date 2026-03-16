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
from urllib.parse import quote_plus

import requests
import openai

# Paths
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content" / "posts"

# Algolia HN Search API (supports time-range queries)
HN_SEARCH_API = "https://hn.algolia.com/api/v1/search"

# OpenAI
OPENAI_MODEL = "gpt-4o"


def get_recent_top_stories(n=50):
    """Fetch top HN stories from the past 7 days using Algolia search API."""
    cutoff = int(time.time() - 7 * 86400)

    resp = requests.get(HN_SEARCH_API, params={
        "tags": "story",
        "numericFilters": f"created_at_i>{cutoff},points>10",
        "hitsPerPage": n,
    }, timeout=15)
    resp.raise_for_status()

    stories = []
    for hit in resp.json().get("hits", []):
        url = hit.get("url")
        if not url:
            continue
        stories.append({
            "title": hit.get("title", "Untitled"),
            "url": url,
            "score": hit.get("points", 0),
            "comments": hit.get("num_comments", 0),
            "author": hit.get("author", "unknown"),
            "hn_url": f"https://news.ycombinator.com/item?id={hit['objectID']}",
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

    system_prompt = """You are a friendly tech writer for a developer blog. You write like a real person — casual, clear, and easy to follow. No corporate jargon, no buzzwords, no filler. Just plain language that anyone in tech can enjoy reading.

You will receive a list of trending tech stories from the past week.

Your task:
1. Select the 15 most significant and interesting stories.
2. Place each story into one of these EXACT four categories:
   - "Technology and Tools" — new tools, frameworks, languages, hardware, infrastructure
   - "Open Source and Development" — open source projects, developer workflows, coding practices
   - "AI News" — anything related to AI, LLMs, machine learning, data science
   - "Notable Voices" — opinions, hot takes, or notable statements from well-known people in tech (founders, engineers, researchers, etc.). If someone important said something interesting or controversial, it goes here.
3. For each story, write a 2-3 sentence summary. Write naturally — like you're telling a friend about it over coffee. Keep it simple and conversational. Do NOT sound like AI or a press release. Avoid phrases like "This marks a significant", "This development", "notable for its", etc.
4. Write a short, friendly intro paragraph (2-3 sentences) for the weekly digest. Do NOT mention Hacker News as the source.
5. Write 3-4 thought-provoking questions at the end that make readers think about the week's news. These should be open-ended and genuinely interesting, not generic.
6. Suggest relevant tags (lowercase, hyphenated, e.g. "machine-learning").

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
  "questions": ["question1", "question2", "question3"],
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


def generate_cover_image(digest_data, post_dir):
    """Use DALL-E to generate a cover image based on the week's top stories."""
    # Collect top story summaries for a more specific image
    top_stories = []
    for cat in digest_data.get("categories", []):
        for story in cat.get("stories", [])[:2]:
            top_stories.append(
                f"- {story['title']}: {story.get('summary', '')}"
            )

    stories_context = "\n".join(top_stories[:5])

    prompt = (
        "Create a vivid, photorealistic editorial illustration for a tech news article cover. "
        "The image should visually represent these specific stories:\n"
        f"{stories_context}\n\n"
        "Show recognizable visual elements: company logos as physical objects, "
        "country landmarks, devices, or silhouettes of people in relevant settings. "
        "For example, if a story is about Apple, show an Apple product; if about a country's tech policy, "
        "show that country's landmark. Make it feel like a magazine cover photo collage. "
        "Absolutely NO text, NO words, NO letters, NO labels anywhere in the image. "
        "Use dramatic lighting, rich colors, and a cinematic editorial photography style."
    )

    client = openai.OpenAI()
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1792x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    image_data = requests.get(image_url, timeout=60).content

    image_path = post_dir / "cover.png"
    image_path.write_bytes(image_data)
    return "cover.png"


def render_markdown(digest_data, digest_date, cover_image=None):
    """Render the digest data as a Hugo-compatible markdown post."""
    date_str = digest_date.strftime("%Y-%m-%d")
    title = f"Weekly Tech Digest - {digest_date.strftime('%B %d, %Y')}"

    # Build tags list
    base_tags = ["weekly-digest", "tech-news"]
    extra_tags = digest_data.get("tags", [])
    all_tags = sorted(set(base_tags + extra_tags))

    # Frontmatter
    tags_yaml = "\n".join(f'  - "{t}"' for t in all_tags)
    cover_yaml = ""
    if cover_image:
        cover_yaml = f"""
cover:
  image: "{cover_image}"
  alt: "{title}"
  relative: true
  hidden: true"""

    frontmatter = f"""---
title: "{title}"
date: {date_str}
description: "A curated weekly roundup of the most interesting stories in tech"
tags:
{tags_yaml}
categories:
  - "tech-news"{cover_yaml}
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
            search_url = f"https://www.google.com/search?q={quote_plus(story['title'])}"
            body_parts.append(
                f"[Read the article]({story['url']}) · "
                f"[HN Discussion]({story['hn_url']}) · "
                f"[Read more]({search_url})"
                + (f" ({meta})" if meta else "")
                + "\n"
            )

    # Questions section
    questions = digest_data.get("questions", [])
    if questions:
        body_parts.append("\n## Something to Think About\n")
        for q in questions:
            body_parts.append(f"- {q}")
        body_parts.append("")

    return frontmatter + "\n\n" + "\n".join(body_parts)



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

    # Create post directory early so we can save the cover image into it
    slug = f"weekly-tech-digest-{digest_date.strftime('%Y-%m-%d')}"
    post_dir = CONTENT_DIR / slug
    post_dir.mkdir(parents=True, exist_ok=True)

    print("Generating cover image with DALL-E...")
    cover_image = None
    try:
        cover_image = generate_cover_image(digest_data, post_dir)
    except (openai.OpenAIError, requests.RequestException) as e:
        print(f"Warning: Could not generate cover image: {e}", file=sys.stderr)
        print("Continuing without cover image...")

    print("Generating markdown post...")
    markdown = render_markdown(digest_data, digest_date, cover_image)

    print("Writing post file...")
    post_file = post_dir / "index.md"
    post_file.write_text(markdown, encoding="utf-8")
    print(f"Post written to: {post_file}")


if __name__ == "__main__":
    main()
