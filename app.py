from flask import Flask, render_template, request, send_from_directory, jsonify, make_response
from flask_cors import CORS
import yt_dlp
import os
import time
import threading

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

download_progress = {}
download_results = {}


def make_progress_hook(task_id, file_id):
    def progress_hook(d):
        if d['status'] == 'downloading':
            pct = d.get('_percent_str', '0%').replace('%', '').strip()
            try:
                download_progress[task_id][file_id] = float(pct)
            except:
                download_progress[task_id][file_id] = 0

        elif d['status'] == 'finished':
            download_progress[task_id][file_id] = 100

    return progress_hook


def download_task(urls, download_type, task_id):
    download_progress[task_id] = {}
    results = []

    for i, url in enumerate(urls):
        file_id = f"{task_id}_{i}"
        download_progress[task_id][file_id] = 0

        try:
            options = {
                'outtmpl': f'{DOWNLOAD_FOLDER}/%(title).100s_{int(time.time())}.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'restrictfilenames': True,
                'progress_hooks': [make_progress_hook(task_id, file_id)],
            }

            if download_type == "audio":
                options.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                    }]
                })

            elif download_type == "video":
                options.update({
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                    'merge_output_format': 'mp4'
                })

            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=True)

                filename = ydl.prepare_filename(info)

                if download_type == "audio":
                    filename = os.path.splitext(filename)[0] + ".mp3"
                else:
                    filename = os.path.splitext(filename)[0] + ".mp4"

                # ✅ FORCE COMPLETE
                download_progress[task_id][file_id] = 100

                results.append({
                    "file": os.path.basename(filename),
                    "id": file_id
                })

        except Exception as e:
            results.append({
                "file": f"Error: {url}",
                "id": file_id
            })
            download_progress[task_id][file_id] = 100

    download_results[task_id] = results

@app.route("/api/start", methods=["POST"])
def api_start():
    data = request.json
    urls = data.get("urls", [])
    download_type = data.get("type", "video")

    task_id = str(time.time())

    thread = threading.Thread(
        target=download_task,
        args=(urls, download_type, task_id)
    )
    thread.start()

    return {"task_id": task_id}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_download():
    urls = request.form["urls"].splitlines()
    download_type = request.form["type"]

    urls = [u.strip() for u in urls if u.strip()]
    task_id = str(time.time())

    thread = threading.Thread(
        target=download_task,
        args=(urls, download_type, task_id)
    )
    thread.start()

    return jsonify({"task_id": task_id, "count": len(urls)})


@app.route("/progress/<task_id>")
def progress(task_id):
    return jsonify({
        "progress": download_progress.get(task_id, {}),
        "files": download_results.get(task_id, [])
    })


@app.route("/download/<path:filename>")
def download_file(filename):
    response = make_response(
        send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=False)
    )
    response.headers["Cache-Control"] = "no-store"
    return response


if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)