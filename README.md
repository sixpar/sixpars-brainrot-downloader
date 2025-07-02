# Sixpar's Brainrot Downloader

A self-hosted web app to download TikToks, Instagram Reels, and YouTube videos as MP4, WebM, or MP3. Includes a Discord-optimized option for easy sharing!

## Features
- Download TikTok, Instagram, and YouTube videos
- Choose output format: MP4, WebM, or MP3
- Optional Discord-optimized re-encoding (H.264/AAC, 720p, smaller size)
- Videos auto-delete after 1 minute
- Simple web UI

## Quick Start

1. **Install Docker and Docker Compose**
   - [Docker Install Guide](https://docs.docker.com/get-docker/)
   - [Docker Compose Install Guide](https://docs.docker.com/compose/install/)

2. **Clone or copy this folder to your server:**
   ```sh
   git clone <this-repo-url> sixpars-brainrot-downloader
   cd sixpars-brainrot-downloader
   ```
   *(Or just copy the folder if you received it directly)*

3. **Build and start the server:**
   ```sh
   docker compose up -d --build
   ```

4. **Open your browser to:**
   - `http://localhost:5000` (if running locally)
   - `http://<your-server-ip>:5000` (if running on a server)

## Notes
- Videos are deleted after 1 minute for privacy and storage management.
- For Discord-optimized downloads, check the box on the web UI.
- If you want to use Instagram cookies, add your `instagram_cookies.txt` to the project folder.

## Folder Structure
```
.
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── templates/
│   └── index.html
├── downloads/           # Downloaded files (auto-cleaned)
└── README.md
```

---

**Made with ❤️ by Sixpar** 