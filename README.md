<div align="center">
  <h1>CleanURL 🚀</h1>
  <p><strong>Simple URL shortener</strong> built with <strong>FastAPI</strong>. Convert long URLs into short, shareable links and redirect users automatically.</p>
  <p>
    <img src="https://img.shields.io/badge/python-3.11-blue.svg" alt="Python" />
    <img src="https://img.shields.io/badge/fastapi-%239AD8FF.svg?style=flat&logo=fastapi&logoColor=white" alt="FastAPI" />
  </p>
</div>

–––

## Challenge

Avito livecoding task https://solvit.space/test-tasks/3

---

## Overview

CleanURL is a minimal, async URL shortener using FastAPI and SQLAlchemy. It's designed to be lightweight and easy to run locally or in Docker — ideal for learning or small projects.

---

## Features

- Generate short URLs from long links
- Redirect via short URL
- Async & lightweight with SQLAlchemy
- Easy to run locally or in Docker

---

## Project Structure

```
CleanURL/
├─ main.py
├─ service.py
├─ database/
│  ├─ db.py
  └─ models.py
├─ exceptions.py
└─ README.md
```

---

## API Endpoints 🌐

### POST /short_url — generate a short link

Request JSON:

```json
{
  "long_url": "https://example.com"
}
```

Response JSON:

```json
{
  "slug": "abc123"
}
```

### GET /{slug} — redirect to the original URL

Example:

```bash
curl http://localhost:8000/abc123
# redirects to https://example.com
```