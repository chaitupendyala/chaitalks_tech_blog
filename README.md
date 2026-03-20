# ChaiTalks.Tech

A personal tech blog about AI, software engineering, and interesting projects — built with [Hugo](https://gohugo.io/) and the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme, deployed on [Cloudflare Pages](https://pages.cloudflare.com/).

**Live site:** [https://chaitalks.tech](https://chaitalks.tech)

## Tech Stack

- **Static Site Generator:** Hugo
- **Theme:** PaperMod
- **Hosting:** Cloudflare Pages
- **Comments:** Giscus (GitHub Discussions-backed)
- **Automation:** Python 3.12 + GitHub Actions (weekly tech digest)
- **AI Integration:** OpenAI GPT-4o for content summarization

## Features

- **Full-text search** across posts and tags
- **Reading progress bar** on articles
- **Code block enhancements** — copy-to-clipboard buttons and language badges
- **Giscus comments** with automatic dark/light theme sync
- **Push notifications** via service worker for new content
- **Series navigation** for multi-part posts
- **Breadcrumb navigation**
- **Weekly Tech Digest** — automated curation of trending Hacker News stories, summarized with AI

## Getting Started

### Prerequisites

- [Hugo](https://gohugo.io/installation/) (extended edition recommended)
- Git
- Python 3.12+ (only needed for the weekly digest script)

### Setup

```bash
# Clone the repository
git clone https://github.com/chaitupendyala/chaitalks_tech_blog.git
cd chaitalks_tech_blog

# Initialize the PaperMod theme submodule
git submodule update --init --recursive
```

### Local Development

```bash
hugo server
# Site available at http://localhost:1313
```

### Production Build

```bash
./build.sh
# or directly:
hugo --minify
```

The built site is output to the `public/` directory.

## Weekly Tech Digest

A GitHub Actions workflow runs every Sunday to automatically generate a weekly tech digest:

1. Fetches the top 50 trending stories from Hacker News (past 7 days)
2. Uses OpenAI GPT-4o to summarize and categorize stories
3. Generates a Hugo blog post and opens a pull request for review

To run locally:

```bash
pip install -r scripts/requirements.txt
export OPENAI_API_KEY="your-key"
python scripts/weekly_tech_digest.py
```

## Project Structure

```
├── content/
│   ├── posts/           # Blog articles
│   ├── apps/            # Apps/projects showcase
│   └── digest/          # Weekly tech digest archive
├── layouts/
│   ├── partials/        # Custom components (header, footer, comments)
│   └── _default/        # Page templates
├── scripts/
│   └── weekly_tech_digest.py   # Digest generation script
├── static/              # Static assets (logo, favicons)
├── themes/PaperMod/     # Theme (git submodule)
├── hugo.toml            # Hugo configuration
├── wrangler.toml        # Cloudflare Pages configuration
└── build.sh             # Build script
```

## Deployment

The site is deployed to Cloudflare Pages. Configuration is in `wrangler.toml`:

- **Build command:** `./build.sh`
- **Output directory:** `./public`

Pushes to the main branch trigger automatic deployments.
