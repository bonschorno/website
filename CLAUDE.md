# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Start local dev server with live reload
hugo server

# Build for production
hugo

# Create new content
hugo new content/<section>/<filename>.md
```

## Architecture

This is a [Hugo](https://gohugo.io/) static site using the **typo** theme (git submodule at `themes/typo`, sourced from https://github.com/tomfran/typo).

- **`hugo.toml`** — site config: base URL, title, nav menu items, and social links
- **`content/`** — Markdown pages with TOML front matter (`+++...+++`)
- **`public/`** — static assets served as-is: custom fonts (Literata, Monaspace), favicons, and JS (theme switcher, copy-code, mermaid)
- **`themes/typo/`** — do not edit; it's a git submodule. Override theme layouts by mirroring paths under a top-level `layouts/` directory

## Content conventions

- Pages use TOML front matter delimiters (`+++`)
- Section index pages are named `_index.md`
- Add pages to the nav menu by adding `[[params.menu]]` entries in `hugo.toml`
- Add social links via `[[params.social]]` in `hugo.toml`; icon names come from [Simple Icons](https://simpleicons.org/)
