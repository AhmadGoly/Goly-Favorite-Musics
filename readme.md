# Trackify Artist Bot - Project Purpose & Architecture

## Project Reason & Purpose

This project started as a way to easily track new song releases from favorite artists directly via Telegram.  
The initial implementation was done in Python, leveraging the **MusicBrainz API** to fetch detailed artist release data. The goal was to have a convenient, automated way for music fans to keep updated without manually checking multiple sources.

---

## Python Part

- **Role:** Prototype and proof of concept  
- **Functionality:**  
  - Connects to the MusicBrainz API to search artists by name.  
  - Fetches all releases and tracks for an artist, including release dates.  
  - Normalizes dates and sorts tracks to find the newest releases.  
- **Outcome:**  
  - Demonstrated how to extract and process music data from MusicBrainz.  
  - Provided the logic and data flow blueprint for the Telegram bot.

---

## JavaScript Part (Cloudflare Worker)

- **Role:** Production-ready Telegram bot running serverless on Cloudflare Workers.  
- **Functionality:**  
  - Implements Telegram webhook to receive user commands and respond asynchronously.  
  - Uses the logic derived from the Python prototype for fetching new songs via the MusicBrainz API.  
  - Manages user-specific data such as favorite artist groups with persistent storage in Cloudflare Workers KV.  
  - Handles user commands for creating groups, adding/removing artists, and querying new songs.  
- **Benefits:**  
  - Serverless, scalable, and fast response with minimal infrastructure overhead.  
  - Persistent and personalized user data management.  
  - Clean separation of concerns using modular JS functions for maintainability.

---

## Overall Architecture

1. User sends commands to Telegram bot.
2. Telegram forwards the update to Cloudflare Worker webhook.
3. Worker processes commands:
   - For `/NewSongs`, queries MusicBrainz API and returns top new tracks.
   - For group commands, updates or fetches data in KV store.
4. Worker sends formatted response back to the user via Telegram API.

---

## Reason of using Cloudflare Workers

- Instant global deployment close to users.
- Built-in KV storage for lightweight persistence.
- Low latency and easy scaling.
- No server maintenance or infrastructure setup.

---

## Summary

This project blends Python-based data fetching and processing expertise with modern JavaScript serverless deployment to deliver a responsive, user-friendly Telegram bot for music fans worldwide.

