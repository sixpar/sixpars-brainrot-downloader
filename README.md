# Sixpar's Brainrot Downloader

## EZ MODE INSTALLATION (for any box with Docker)

### 🛠️ Get Docker & Docker Compose poppin'

Luh links for the cuhs that need it:
- [Docker Install Guide](https://docs.docker.com/get-docker/)
- [Docker Compose Install Guide](https://docs.docker.com/compose/install/)

---

### 💾 Grab the code, cuh

Best way? Git that shii:

```sh
git clone https://github.com/sixpar/sixpars-brainrot-downloader.git
cd sixpars-brainrot-downloader
```

OR just snatch the ZIP off GitHub n unzip it. Ion care.

---

### 🚀 Spin dat bih up

```sh
docker compose up -d --build
```

KERBLOW 💥 server up. Easy money.

---

### 🌐 Hop in yo browser

- [http://localhost:5000](http://localhost:5000) if you on the same box
- `http://<ya-server-ip>:5000` if you remote wit it

---

### 🍕 WAH-LAH. HERE'S YOUR ZA.

Sit back. Vibe. Let the brainrot flow.

---

### 🔐 (OPTIONAL) Instagram Cookies

Tryna snatch private Reels like a ninja? Drop your `instagram_cookies.txt` in the project folder. Now you VIP in them DMs.

---

### ✅ Done done.

Paste them TikToks, Reels, YouTube links in the web UI.

Pick MP4 / WebM / MP3 — whatever ya soul need.

Videos disappear in 60 seconds like Houdini.

Wanna fit it for Discord? Just tick that luh box 🧠✅

---

### 🧯 If shii break:

- Permissions error? Use sudo or toss yourself in the docker gang.
- Wanna update? Pull dat latest and re-run the build.

```sh
# If you get a permissions error with Docker:
sudo docker compose up -d --build

# Or add yourself to the docker group (then log out and back in):
sudo usermod -aG docker $USER

# To update the app:
git pull
sudo docker compose up -d --build
```

---

✨ Made with way too much love by Sixpar

---

#### this joint powered by:

- 🧪 **yt-dlp** — public domain, go wild
- 🧼 **Flask** — BSD-3
- 🔁 **HandBrakeCLI** — GPL-2.0 or sum shii

Big shoutout to the real ones who built all that. Without y'all, we just out here rottin wit no sauce 💯

---

<sub>^^ the text above was written by AI ^^</sub>

---

## Credits

This project would not be possible without these amazing open-source tools:

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — Unlicense (public domain)
- [Flask](https://flask.palletsprojects.com/) — BSD-3-Clause License
- [HandBrakeCLI](https://handbrake.fr/) — GPL-2.0-only License

Thank you to all the contributors and maintainers of these projects! 