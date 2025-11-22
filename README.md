# CleanURL 🚀

A simple URL shortener built with **FastAPI**. Turn long URLs into short, shareable links and redirect users automatically. Think Bitly, but minimal and async.

---

## Features

- Generate short URLs from long links
- Redirect via short URL
- Async & lightweight with SQLAlchemy
- Easy to run locally or in Docker

---

## Project Structure

CleanURL/
├─ main.py # FastAPI app and routes
├─ service.py # URL generation and retrieval logic
├─ database/
│ ├─ db.py # DB connection
│ └─ models.py # SQLAlchemy models
├─ exceptions.py # Custom exceptions
└─ README.md

---

# API Endpoints 🌐

POST /short_url — generate a short link

Request:
{
  "long_url": "https://example.com"
}

Response:
{
  "slug": "abc123"
}

GET /{slug} — redirect to the original URL

curl http://localhost:8000/abc123
# redirects to https://example.com
