"""
Simple Flask server for health checks and proxying to Local Bot API
Runs on port 10000 (Render's default)
"""
from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
LOCAL_API_URL = 'http://localhost:8081'

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Render"""
    try:
        # Check if Local Bot API is running
        response = requests.get(f'{LOCAL_API_URL}/bot{TELEGRAM_BOT_TOKEN}/getMe', timeout=5)
        if response.status_code == 200:
            return {'status': 'healthy', 'bot_api': 'running'}, 200
    except:
        pass
    return {'status': 'starting', 'bot_api': 'initializing'}, 503

@app.route('/bot<path:path>', methods=['GET', 'POST'])
def proxy_to_bot_api(path):
    """Proxy all /bot* requests to Local Bot API on port 8081"""
    url = f'{LOCAL_API_URL}/bot{path}'
    
    # Forward the request
    if request.method == 'GET':
        resp = requests.get(url, params=request.args, timeout=600)
    else:
        resp = requests.post(
            url,
            data=request.form,
            files=request.files,
            timeout=600
        )
    
    # Return the response
    return Response(
        resp.content,
        status=resp.status_code,
        headers=dict(resp.headers)
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
