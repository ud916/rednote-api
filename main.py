from flask import Flask, request, jsonify, render_template_string
import yt_dlp
import re

app = Flask(_name_)

HTML_CODE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rednote Pro Downloader</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background: #f4f4f4; padding: 20px; }
        .container { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 450px; margin: auto; }
        input, select { width: 90%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
        button { width: 95%; padding: 12px; background: #ff2442; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        #result { margin-top: 20px; }
        video { width: 100%; border-radius: 10px; margin-top: 10px; }
        .loader { color: #ff2442; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2 style="color: #ff2442;">Rednote Saver Pro</h2>
        <input type="text" id="videoUrl" placeholder="Paste Rednote link here...">
        
        <select id="quality">
            <option value="480">480p (Small Size)</option>
            <option value="720" selected>720p (Normal - Recommended)</option>
            <option value="1080">1080p (Full HD)</option>
            <option value="1440">2K (High Quality)</option>
            <option value="2160">4K (Ultra HD)</option>
        </select>

        <button onclick="downloadVideo()">Process Video</button>
        <div id="result"></div>
    </div>

    <script>
        async function downloadVideo() {
            const url = document.getElementById('videoUrl').value;
            const quality = document.getElementById('quality').value;
            const resDiv = document.getElementById('result');
            
            if(!url) return alert("Link paste karein!");
            resDiv.innerHTML = "<p class='loader'>Fetching best link for " + quality + "p... Please wait.</p>";

            try {
                const response = await fetch(/extract?url=${encodeURIComponent(url)}&q=${quality});
                const data = await response.json();

                if(data.status === "success") {
                    resDiv.innerHTML = `
                        <p><strong>${data.title}</strong></p>
                        <video controls><source src="${data.video_url}" type="video/mp4"></video>
                        <br><br>
                        <a href="${data.video_url}" target="_blank" style="text-decoration:none; background:green; color:white; padding:10px; border-radius:5px; display:inline-block;">Download / Save</a>
                    `;
                } else {
                    resDiv.innerHTML = "<p style='color:red;'>Error: " + data.message + "</p>";
                }
            } catch (error) {
                resDiv.innerHTML = "<p style='color:red;'>Server Error!</p>";
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/extract')
def extract():
    raw_input = request.args.get('url')
    quality = request.args.get('q', '720')
    
    url_match = re.search(r'(https?://[^\s]+)', raw_input)
    if not url_match:
        return jsonify({"status": "error", "message": "Link sahi nahi hai!"})
    
    video_url = url_match.group(1)

    # Quality setting logic
    fmt = f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]"

    ydl_opts = {
        'format': fmt,
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
        'socket_timeout': 30,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            # Kuch cases mein 'url' direct nahi hota, formats check karne padte hain
            best_url = info.get('url')
            if not best_url and 'formats' in info:
                best_url = info['formats'][-1]['url']

            return jsonify({
                "status": "success",
                "video_url": best_url,
                "title": info.get('title', 'Rednote Video')
            })
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)