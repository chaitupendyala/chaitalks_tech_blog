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

The Machine Control Protocol (MCP) is quickly becoming a preferred interface for integrating AI capabilities into developer tools, terminals, and other interactive environments. In essence, MCP defines a simple, message-based protocol where _tools_ can respond to structured _commands_—enabling dynamic, programmable extensions to your application.

In this article, we’ll walk through how to build your own MCP server using Python. We'll use the [`fastmcp`](https://pypi.org/project/fastmcp/) library for quickly defining and serving tools, and [`uv`](https://github.com/astral-sh/uv), a new blazing-fast Python package manager, to manage dependencies and environments.

* * *

### What is MCP?

At a high level, MCP (Machine Control Protocol) is a way to extend applications with programmable tools. Think of it like an intelligent command palette that responds to structured inputs. Instead of parsing raw text like a shell or CLI, MCP tools receive JSON-formatted commands with metadata, arguments, and context—and return structured results.

This makes it especially powerful for AI integrations, developer tooling, and interactive automation.

* * *

### Tools We’ll Use

1. **[`uv`](https://github.com/astral-sh/uv)** — a fast, modern Python package manager (a drop-in replacement for pip, but written in Rust and much faster).

3. **[`fastmcp`](https://pypi.org/project/fastmcp/)** — a Python library that simplifies building and serving MCP tools using decorators.

* * *

### Getting Started

#### 1\. Initialize Your Project

```
mkdir mcp-server-example
cd mcp-server-example
uv venv
source .venv/bin/activate
uv pip install fastmcp
```

* * *

### 2\. Build the MCP Server

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

Then run your server:

```
uv run main.py
```

By default, this will start on `http://localhost:8000`.

You now have an MCP server with one tool: `read_file`.

* * *

## Integrating with ChatGPT

MCP servers can be connected directly to **custom GPTs** using the [**MCP Tools Interface**](https://platform.openai.com/docs/gpts/mcp-tools). Here's how:

### 1\. Deploy Your Server

You’ll need to make your MCP server publicly accessible. Two options:

- **Local testing**: Use [ngrok](https://ngrok.com/) to expose your local server: `grok http 8000`

- **Production**: Deploy it to a platform like Render, Fly.io, Railway, or your VPS.

This will give you a public URL like `https://abc123.ngrok.io`.

* * *

### 2\. Create a Custom GPT

1. Go to [ChatGPT → Explore GPTs](https://chat.openai.com/gpts/explore)

3. Click **Create** → fill out basic info

5. Under **"Add Actions"**, choose **"MCP"**

7. Paste your MCP server URL (e.g. `https://abc123.ngrok.io`)

9. The GPT will auto-discover tools like `read_file`!

Now you can chat with your GPT like:

```
Can you show me what's in my config.txt file?
```

Behind the scenes, ChatGPT turns this into a tool call to `read_file(filename="config.txt")` and shows the result.

* * *

## Extending Your MCP Server

You can define multiple tools in your MCP server using the same pattern:

```
@app.tool(name="list_files", description="Lists files in a directory.")
def list_files(directory: str = ".") -> list[str]:
    import os
    try:
        return os.listdir(directory)
    except Exception as e:
        return [f"Error: {str(e)}"]
```

These tools become immediately usable inside ChatGPT or other MCP clients—without writing any extra frontend or CLI parsing logic.

* * *

## Possibilities and Use Cases

Here’s where it gets interesting:

- **Developer assistants**: Expose project-specific tools like `run_tests`, `lint_code`, or `deploy_app`.

- **Personal AI agents**: Let ChatGPT control files, databases, web APIs, or smart home tools.

- **Serverless operations**: Run simple MCP tools in containers or lambdas and connect on-demand.

- **AI Automation**: Turn ChatGPT into a programmable agent over your infrastructure.

You can even add **auth**, **context-awareness**, or connect to your own APIs and databases to power workflows with intelligence and control.

* * *

## Final Thoughts

With just a few lines of Python, you’ve built a powerful, extensible interface between code and AI. The combination of **FastMCP** and **ChatGPT’s MCP support** opens a new era of developer productivity and custom AI tooling.

Want to go further? Try combining:

- `openai` API for LLM-powered responses inside your tools

- database tools like `sqlite3` or `SQLAlchemy`

- automation packages like `subprocess`, `paramiko`, or `requests`
