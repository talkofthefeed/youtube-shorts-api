import os
import uuid
import json
from flask import Flask, request, jsonify, send_from_directory
import yt_dlp
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

# Ensure downloads directory exists
DOWNLOADS_DIR = 'downloads'
if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

@app.route('/')
def home():
    return jsonify({
        "message": "YouTube Shorts Downloader API",
        "usage": "/download?url=<youtube_shorts_url>",
        "example": "/download?url=https://youtube.com/shorts/VIDEO_ID"
    })

@app.route('/download')
def download_video():
    try:
        # Get URL from query parameters
        url = request.args.get('url')
        if not url:
            return jsonify({
                "status": "error",
                "message": "Missing 'url' parameter"
            }), 400
        
        # Validate YouTube URL
        if 'youtube.com' not in url and 'youtu.be' not in url:
            return jsonify({
                "status": "error",
                "message": "Invalid YouTube URL"
            }), 400
        
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        output_filename = f"{unique_id}.%(ext)s"
        output_path = os.path.join(DOWNLOADS_DIR, output_filename)
        
        # yt-dlp options for highest quality
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': output_path,
            'noplaylist': True,
        }
        
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'Unknown')
        
        # Find the actual downloaded file
        downloaded_file = None
        for file in os.listdir(DOWNLOADS_DIR):
            if file.startswith(unique_id):
                downloaded_file = file
                break
        
        if not downloaded_file:
            return jsonify({
                "status": "error",
                "message": "Download failed - file not found"
            }), 500
        
        # Get the base URL (Railway provides this automatically)
        base_url = request.url_root.rstrip('/')
        download_url = f"{base_url}/downloads/{downloaded_file}"
        
        return jsonify({
            "status": "success",
            "title": video_title,
            "filename": downloaded_file,
            "download_url": download_url
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Download failed: {str(e)}"
        }), 500

@app.route('/downloads/<filename>')
def serve_download(filename):
    """Serve downloaded files as static content"""
    try:
        return send_from_directory(DOWNLOADS_DIR, filename, as_attachment=False)
    except FileNotFoundError:
        return jsonify({
            "status": "error",
            "message": "File not found"
        }), 404

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "downloads_count": len(os.listdir(DOWNLOADS_DIR))
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
