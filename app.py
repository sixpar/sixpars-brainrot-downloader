import os
import threading
import time
import uuid
from flask import Flask, render_template, request, send_from_directory, jsonify
import yt_dlp
import subprocess

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

progress_dict = {}

def cleanup_file(filepath, delay=60):
    time.sleep(delay)
    if os.path.exists(filepath):
        os.remove(filepath)

def download_video(url, video_id):
    print(f"[DEBUG] Starting download for {url} as {video_id}")
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.%(ext)s")
    ydl_opts = {
        'outtmpl': output_path,
        'progress_hooks': [lambda d: progress_hook(d, video_id)],
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            progress_dict[video_id]['status'] = 'finished'
    except Exception as e:
        print(f"[ERROR] yt-dlp failed for {video_id}: {e}")
        progress_dict[video_id]['status'] = 'error'
        progress_dict[video_id]['error'] = str(e)
        return

    # Convert to .webm using ffmpeg
    webm_filename = os.path.splitext(filename)[0] + '.webm'
    ffmpeg_cmd = [
        'ffmpeg', '-y', '-i', filename,
        '-c:v', 'libvpx', '-b:v', '1M', '-c:a', 'libvorbis',
        '-threads', '1',
        webm_filename
    ]
    try:
        subprocess.run(ffmpeg_cmd, check=True)
    except subprocess.CalledProcessError as e:
        progress_dict[video_id]['status'] = 'error'
        progress_dict[video_id]['error'] = f'ffmpeg failed: {e}'
        return
    # Optionally, delete the original file after conversion
    try:
        os.remove(filename)
    except Exception:
        pass

    # List files in downloads dir for debugging
    print(f"[DEBUG] Files in downloads after download for {video_id}: {os.listdir(DOWNLOAD_FOLDER)}")
    # Clean up both possible extensions
    for ext in ["webm", "mp4"]:
        threading.Thread(target=cleanup_file, args=(os.path.join(DOWNLOAD_FOLDER, f"{video_id}.{ext}"),)).start()

def progress_hook(d, video_id):
    if video_id not in progress_dict:
        progress_dict[video_id] = {'progress': 0, 'status': 'downloading'}
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 1
        downloaded = d.get('downloaded_bytes', 0)
        progress = int(downloaded / total * 100)
        progress_dict[video_id]['progress'] = progress
    elif d['status'] == 'finished':
        progress_dict[video_id]['progress'] = 100
        progress_dict[video_id]['status'] = 'processing'

def run_download(url, download_type, download_id, progress_dict, discord_opt=False):
    use_instagram_cookies = 'instagram.com' in url.lower()
    cookies_file = 'instagram_cookies.txt'
    if download_type == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{download_id}.%(ext)s'),
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        if use_instagram_cookies and os.path.exists(cookies_file):
            ydl_opts['cookiefile'] = cookies_file
            ydl_opts['http_headers'] = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    elif download_type == 'webm':
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'webm',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{download_id}.%(ext)s'),
            'quiet': True,
        }
        if use_instagram_cookies and os.path.exists(cookies_file):
            ydl_opts['cookiefile'] = cookies_file
            ydl_opts['http_headers'] = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    else:  # mp4
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{download_id}.%(ext)s'),
            'quiet': True,
        }
        if use_instagram_cookies and os.path.exists(cookies_file):
            ydl_opts['cookiefile'] = cookies_file
            ydl_opts['http_headers'] = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if download_type == 'mp3':
                filename = os.path.splitext(filename)[0] + '.mp3'
            elif download_type == 'webm':
                filename = os.path.splitext(filename)[0] + '.webm'
            # If Discord-optimized is requested and it's a YouTube video, re-encode with HandBrakeCLI
            if discord_opt and ("youtube.com" in url or "youtu.be" in url) and download_type in ["mp4", "webm"]:
                discord_filename = os.path.splitext(filename)[0] + "_discord.mp4"
                handbrake_cmd = [
                    "HandBrakeCLI", "-i", filename, "-o", discord_filename,
                    "-e", "x264", "-q", "28", "-B", "96", "--optimize",
                    "--maxWidth", "1280", "--maxHeight", "720"
                ]
                try:
                    subprocess.run(handbrake_cmd, check=True)
                    # Optionally, delete the original file after re-encoding
                    try:
                        os.remove(filename)
                    except Exception:
                        pass
                    filename = discord_filename
                except subprocess.CalledProcessError as e:
                    progress_dict[download_id]['status'] = 'error'
                    progress_dict[download_id]['error'] = f'HandBrake failed: {e}'
                    return
            progress_dict[download_id]['status'] = 'finished'
            progress_dict[download_id]['filename'] = os.path.basename(filename)
    except Exception as e:
        progress_dict[download_id]['status'] = 'error'
        progress_dict[download_id]['error'] = str(e)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", status="")

@app.route("/download", methods=["POST"])
def download():
    # Supports TikTok, Instagram, and YouTube URLs (and most sites supported by yt-dlp)
    print('DEBUG: request.form =', dict(request.form))
    print('DEBUG: request.files =', dict(request.files))
    url = request.form['url']
    download_type = request.form.get('type', 'mp3')
    discord_opt = request.form.get('discord', 'off') == 'on'
    download_id = str(uuid.uuid4())
    progress_dict[download_id] = {'status': 'downloading', 'progress': 0}
    threading.Thread(target=run_download, args=(url, download_type, download_id, progress_dict, discord_opt)).start()
    return jsonify({'download_id': download_id})

@app.route("/progress/<video_id>")
def progress(video_id):
    return jsonify(progress_dict.get(video_id, {'progress': 0, 'status': 'unknown'}))

@app.route("/video/<video_id>")
def video(video_id):
    for ext in ["webm", "mp4"]:
        filename = f"{video_id}.{ext}"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
    return "File not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
