# 🎬 YouTube Video & Audio Downloader (Flask + yt-dlp)

## 📌 Overview

This project is a web-based YouTube downloader built with Python and Flask.
It allows users to download videos or extract audio from YouTube links through a simple browser interface.

The application supports:

* 🎥 Video download (MP4)
* 🎧 Audio extraction (MP3)
* 📊 Real-time download progress tracking
* 📂 Multiple URL batch processing
* Run under python 3.14.2

---

## 🚀 Features

### ✅ 1. Web UI Input

* Users can input one or multiple YouTube URLs
* Choose download type:

  * Video (MP4)
  * Audio (MP3)

### ✅ 2. Background Download Processing

* Uses `yt-dlp` to handle downloads
* Runs downloads in a separate thread to avoid blocking the UI

### ✅ 3. Real-Time Progress Tracking

* Each download task has a unique `task_id`
* Progress is tracked per file using `progress_hooks`
* Frontend polls backend API to update progress bars

### ✅ 4. File Management

* Files are saved locally in a `/downloads` folder
* Filenames are based on original YouTube titles
* Safe filename handling (restricted characters)

### ✅ 5. Built-in Media Playback

* Downloaded files can be:

  * 🎧 Played directly in browser (audio)
  * 🎥 Watched directly in browser (video)
* Also supports direct download via link

---

## 🏗️ Architecture

### 🔹 Backend (Flask - `app.py`)

* Handles:

  * API requests
  * Download processing
  * Progress tracking
  * File serving

#### Key Endpoints:

* `/` → Web UI
* `/start` → Start download (UI form)
* `/api/start` → Start download (API for apps)
* `/progress/<task_id>` → Get download progress
* `/download/<filename>` → Serve downloaded file

#### Core Components:

* `download_task()` → Executes download using yt-dlp
* `progress_hooks` → Tracks download percentage
* `download_progress` → Stores live progress
* `download_results` → Stores completed files

---

### 🔹 Frontend (HTML - `index.html`)

* Simple UI built with HTML + Jinja2
* Features:

  * URL input (multi-line)
  * Download type selection
  * Dynamic progress display
  * Media playback (audio/video)
  * Download links

---

## ⚙️ Technologies Used

* Python 3
* Flask
* yt-dlp
* FFmpeg (for audio extraction)
* HTML / Jinja2

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/goldmanau/youtubedownloaderUI.git
cd youtubedownloaderUI
```

### 2. Install dependencies

```bash
pip install flask yt-dlp flask-cors
```

### 3. Install FFmpeg

Required for audio extraction (MP3)

* Windows: https://ffmpeg.org/download.html
* Ensure FFmpeg is added to PATH

---

## ▶️ Run the Application

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

Or access from mobile:

```
http://<your-local-ip>:5000
```

---

## 📁 Project Structure

```
project/
│
├── app.py
├── templates/
│   └── index.html
├── downloads/
└── README.md
```

---

## ⚠️ Notes

* Download speed depends on network and YouTube source
* Some formats may vary depending on availability
* Browser playback works best with MP3 and MP4 formats

---

## 🔮 Future Improvements

* Android mobile app integration
* Multiple simultaneous progress bars
* File management UI (delete/history)
* Download queue system
* Docker deployment

---

## 🙌 Acknowledgements

* yt-dlp project: https://github.com/yt-dlp/yt-dlp
* Flask framework: https://flask.palletsprojects.com/

---

## 📜 License

This project is for educational purposes only.
Please respect YouTube’s terms of service when using this tool.
