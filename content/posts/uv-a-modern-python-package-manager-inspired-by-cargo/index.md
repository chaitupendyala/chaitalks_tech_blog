---
title: "UV: A Modern Python Package Manager Inspired by Cargo"
date: 2025-05-19
categories: 
  - "programming-languages"
  - "python"
tags: 
  - "cargo"
  - "dependency-management"
  - "developer-tools"
  - "pip"
  - "pipx"
  - "python"
  - "python-packaging"
  - "rust"
  - "uv"
  - "virtualenv"
---

Python packaging has always been a bit of a mess. You've got `pip` for installing packages, `virtualenv` or `venv` for managing environments, `pip-tools` or `poetry` if you want lockfiles, and `pipx` for globally installed tools. They all work, but gluing them together gets old fast.

**[UV](https://github.com/astral-sh/uv)** is an attempt to replace all of that with one fast, coherent tool. It's written in Rust, built by the team at Astral, and draws pretty heavily on the design of Cargo, Rust's package manager. If you've used Cargo and then gone back to pip, you already know why something like UV is appealing.

* * *

## What UV Actually Does

UV is designed to be a **drop-in replacement for pip**, but it goes further than that. It handles package installation, dependency resolution, virtual environment management, and script running, all in a single binary.

The headline feature is speed. UV is dramatically faster than pip on large installs, often 10x or more, because it's written in Rust and does much smarter parallel work under the hood.

Beyond speed:

- **Lockfiles**: UV has native support for `uv.lock`, which means reproducible installs without needing pip-tools on the side.
- **Built-in environments**: No separate `virtualenv` install needed. UV manages environments as a first-class concept.
- **Hash verification**: Dependencies are verified by hash by default, which pip doesn't do out of the box.

| Feature | pip | UV |
| --- | --- | --- |
| **Performance** | Slower, especially on large installs | Extremely fast (10x or more in many cases) |
| **Lockfile Support** | Delegated to pip-tools or poetry | Native `uv.lock` |
| **Virtual Environment Handling** | Requires `virtualenv` or `venv` | Built-in |
| **Security** | No hash-checking by default | Hash-based verification |
| **Unified Tooling** | pip + pipx + virtualenv + pip-tools | One binary |

* * *

## Using UV in Practice

#### Installing UV

```
cargo install --git https://github.com/astral-sh/uv uv
```

Or check the [official installation docs](https://docs.astral.sh/uv/getting-started/installation/) for your platform.

#### Starting a New Project

```
$ uv init hello-world
$ cd hello-world
```

UV creates:

```
.
├── .python-version
├── README.md
├── main.py
└── pyproject.toml
```

See the [project guide](https://docs.astral.sh/uv/guides/projects/) for more on what these files do.

#### Adding Packages

```
$ uv add requests

$ uv add 'requests==2.31.0'

$ uv add git+https://github.com/psf/requests
```

More on [managing dependencies](https://docs.astral.sh/uv/guides/projects/#managing-dependencies).

#### Virtual Environments

```
# Create default .venv
uv venv

# Create with a custom name
uv venv my-name
```

One nice thing: when you use the default `.venv`, UV finds and uses it automatically. You don't have to manually activate it for most operations.

See the [environments docs](https://docs.astral.sh/uv/pip/environments/) for the full picture.

* * *

## Where It Falls Short

UV is under active development, which means some rough edges:

- Not all pip features are supported yet. Edge cases with certain build backends or PEPs may not work as expected.
- Migrating a large existing project takes some care, especially if your workflow depends on specific pip behavior.
- Teams used to the pip + virtualenv + pip-tools stack will need a bit of time to adjust.

That said, the Astral team ships quickly and the gaps are shrinking. For new projects, there's not much reason not to use it.

* * *

## Worth Trying

UV is the closest thing Python has had to Cargo — a single, fast, opinionated tool that just handles everything. If you've felt the friction of juggling pip, virtualenv, and pip-tools, give it a try on your next project. The speed difference alone is noticeable from the first install.
