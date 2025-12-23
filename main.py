from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "API is Online"

@app.route('/extract')
def extract():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "message": "No URL"})

    # Fast Extraction Settings
    ydl_opts = {
        'format': 'best', # Sabse jaldi link nikalne ke liye
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'extract_flat': False,
        'force_generic_extractor': False
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "status": "success",
                "video_url": info.get('url'),
                "title": info.get('title', 'Video')
            })
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
