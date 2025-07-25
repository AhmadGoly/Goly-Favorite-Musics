# Trackify Artist Telegram Bot - Cloudflare Worker

This project is a Telegram bot deployed on Cloudflare Workers. It helps you track new song releases for your favorite artists and manage custom artist groups directly from Telegram.

---

## Features

- Fetch top 10 newest songs for a given artist with `/NewSongs artist_name`
- Create custom artist groups (e.g. pop, rock, favorites)
- Add or remove artists from your groups
- Delete groups when no longer needed
- Persistent storage of your favorite artists and groups using Cloudflare Workers KV

---

## Setup Instructions

### Prerequisites

- A [Cloudflare account](https://dash.cloudflare.com/sign-up)
- A Telegram bot token (create one with [@BotFather](https://t.me/BotFather))
- Basic familiarity with Cloudflare Workers and KV namespaces

---

### Step 1: Create a Cloudflare Worker

1. Log in to your Cloudflare dashboard.
2. Go to the **Workers** section.
3. Create a new Worker and name it (e.g. `trackify-artist-bot`).

---

### Step 2: Create a KV Namespace

1. In the Workers dashboard, go to **KV** section.
2. Create a new namespace, name it (e.g. `TrackifyArtist`).
3. Bind the namespace to your Worker:
   - Go to your Worker settings.
   - Under **Variables > KV Namespaces**, add a binding named `TrackifyArtist` and select your created namespace.

---

### Step 3: Update your `wrangler.toml`

Make sure your `wrangler.toml` includes the KV binding, example:

```toml
name = "trackify-artist-bot"
type = "javascript"
account_id = "<YOUR_ACCOUNT_ID>"
workers_dev = true

kv_namespaces = [
  { binding = "TrackifyArtist", id = "<YOUR_NAMESPACE_ID>" }
]
