---
title: "Building an MCP Server with Python and FastMCP"
date: 2025-06-16
categories: 
  - "ai"
tags: 
  - "ai-agents"
  - "build-your-own-gpt"
  - "chatgpt-tools"
  - "custom-tools"
  - "developer-productivity"
  - "fastmcp"
  - "mcp"
  - "openai-integration"
  - "python-automation"
  - "uv"
---

MCP is quickly becoming the standard way to give AI models access to external tools and data. Instead of parsing raw text like a shell command, MCP tools receive structured JSON with arguments and context, and return structured results. That makes it much easier to build reliable integrations between AI and real systems.

In this post I'll walk through building a simple MCP server in Python using [`fastmcp`](https://pypi.org/project/fastmcp/) and [`uv`](https://github.com/astral-sh/uv). You'll have something running in a few minutes.

* * *

### What is MCP?

At a high level, MCP (Model Communication Protocol) is a way to extend applications with programmable tools. Think of it like a command palette that speaks structured JSON instead of raw text. Your tools receive typed inputs with metadata and context, and return structured results that the model can reason about.

This makes it particularly useful for AI integrations, developer tooling, and anywhere you want an AI to be able to take actions rather than just produce text.

* * *

### Tools We'll Use

- **[`uv`](https://github.com/astral-sh/uv)** — a fast Python package manager written in Rust. Drop-in replacement for pip, but much faster.
- **[`fastmcp`](https://pypi.org/project/fastmcp/)** — a Python library that lets you define MCP tools using simple decorators.

* * *

### Getting Started

#### 1. Initialize Your Project

```
mkdir mcp-server-example
cd mcp-server-example
uv venv
source .venv/bin/activate
uv pip install fastmcp
```

* * *

### 2. Build the MCP Server

Paste this into `main.py`:

```
from fastmcp import MCPServer, mcp_tool

app = MCPServer()

@app.tool(name="read_file", description="Returns contents of a file given its path.")
def read_file(filename: str) -> str:
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"File not found: {filename}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

if __name__ == "__main__":
    app.serve()
```

Then run it:

```
uv run main.py
```

By default this starts on `http://localhost:8000`. You now have an MCP server with one tool: `read_file`.

* * *

## Connecting to ChatGPT

MCP servers can be wired up to **custom GPTs** via the [MCP Tools Interface](https://platform.openai.com/docs/gpts/mcp-tools).

### 1. Make Your Server Publicly Accessible

Two options:

- **Local testing**: Use [ngrok](https://ngrok.com/) to expose your local port: `ngrok http 8000`
- **Production**: Deploy to Render, Fly.io, Railway, or your own VPS.

This gives you a public URL like `https://abc123.ngrok.io`.

### 2. Create a Custom GPT

1. Go to [ChatGPT → Explore GPTs](https://chat.openai.com/gpts/explore)
2. Click **Create** and fill out the basic info
3. Under **"Add Actions"**, choose **"MCP"**
4. Paste your server URL
5. ChatGPT auto-discovers your tools

Now you can chat with your GPT like:

```
Can you show me what's in my config.txt file?
```

Behind the scenes, ChatGPT turns that into a call to `read_file(filename="config.txt")` and shows you the result.

* * *

## Adding More Tools

Same pattern, just add more decorated functions:

```
@app.tool(name="list_files", description="Lists files in a directory.")
def list_files(directory: str = ".") -> list[str]:
    import os
    try:
        return os.listdir(directory)
    except Exception as e:
        return [f"Error: {str(e)}"]
```

These become immediately usable inside ChatGPT or any other MCP client, no extra CLI parsing or frontend work needed.

* * *

## What You Can Build With This

A few directions worth exploring:

- **Developer assistants**: Expose tools like `run_tests`, `lint_code`, or `deploy_app` so an AI can help with your actual workflow.
- **Personal agents**: Let ChatGPT read files, query a database, or call your own APIs.
- **Automation**: Wire up MCP tools to infrastructure and let an AI drive operations tasks.

You can layer in auth, connect to databases, or chain tools together to build workflows that are actually useful rather than just demos.

* * *

## Final Thoughts

FastMCP makes it pretty low-friction to get an MCP server running. The interesting part starts when you think seriously about what tools to expose and how to make them reliable. But the plumbing itself is surprisingly approachable.

If you want to extend it further, try combining the `openai` SDK for LLM-powered logic inside tools, `sqlite3` or SQLAlchemy for database access, or `subprocess` for running shell commands in a controlled way.
