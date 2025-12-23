from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "OK"

@app.route('/extract')
def extract():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "message": "No URL"})

    # Super fast settings
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "status": "success",
                "video_url": info.get('url'),
                "title": info.get('title', 'Video')
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # Render ke liye port aur host fix
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
