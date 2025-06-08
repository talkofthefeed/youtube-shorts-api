YouTube Shorts Downloader API
A Flask-based REST API that downloads YouTube Shorts videos and serves them via public HTTPS URLs.
🚀 Quick Deploy to Railway
￼
📋 Features
	•	GET /download: Download YouTube Shorts with a simple URL parameter
	•	Static File Serving: Downloaded videos are served as public HTTPS URLs
	•	High Quality: Downloads the best available quality (mp4 preferred)
	•	Unique Filenames: Uses UUID to prevent conflicts
	•	Error Handling: Comprehensive error responses
	•	Health Check: /health endpoint for monitoring
🔧 API Usage
Download a Video
GET /download?url=https://youtube.com/shorts/VIDEO_ID
Response:
{
  "status": "success",
  "title": "Video Title",
  "filename": "abc123-uuid.mp4",
  "download_url": "https://your-app.railway.app/downloads/abc123-uuid.mp4"
}
Access Downloaded Video
GET /downloads/abc123-uuid.mp4
Returns the actual video file for streaming/download.
Health Check
GET /health
Response:
{
  "status": "healthy",
  "downloads_count": 5
}
🛠️ Local Development
	1	Clone and install: pip install -r requirements.txt
	2	
	3	Run the server: python main.py
	4	
	5	Test locally: curl "http://localhost:5000/download?url=https://youtube.com/shorts/VIDEO_ID"
	6	
🌐 Railway Deployment
	1	Push to GitHub (or use Railway CLI)
	2	Connect to Railway: Import your repo
	3	Deploy: Railway auto-detects Python and uses the railway.json config
	4	Get your URL: Railway provides a public HTTPS domain
📝 Integration Examples
n8n Webhook
// n8n HTTP Request Node
{
  "method": "GET",
  "url": "https://your-app.railway.app/download",
  "qs": {
    "url": "{{$json.youtube_url}}"
  }
}
cURL
curl "https://your-app.railway.app/download?url=https://youtube.com/shorts/abc123"
Python Requests
import requests

response = requests.get(
    "https://your-app.railway.app/download",
    params={"url": "https://youtube.com/shorts/abc123"}
)

result = response.json()
video_url = result["download_url"]
⚠️ Notes
	•	Downloaded files are stored in the /downloads/ directory
	•	Files persist until the container restarts (Railway containers are ephemeral)
	•	For production, consider using cloud storage (S3, Google Cloud, etc.)
	•	Rate limiting may be needed for high-traffic usage
	•	Respect YouTube's Terms of Service
🔍 Error Handling
The API returns appropriate HTTP status codes:
	•	200: Success
	•	400: Bad request (missing/invalid URL)
	•	404: File not found
	•	500: Server error (download failed)
All errors include a JSON response with status: "error" and a descriptive message.
