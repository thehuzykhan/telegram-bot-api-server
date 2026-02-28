"""
Simple Flask server for health checks and proxying to Local Bot API
Runs on port 10000 (Render's default)
"""
from flask import Flask, request, Response, render_template_string
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
LOCAL_API_URL = 'http://localhost:8081'

LANDING_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hustlistan Telegram API Server</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: #000000;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }
        
        .container {
            text-align: center;
            z-index: 10;
            position: relative;
        }
        
        .logo {
            font-size: 72px;
            font-weight: 900;
            background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 30px;
            letter-spacing: -2px;
            animation: glow 2s ease-in-out infinite;
        }
        
        @keyframes glow {
            0%, 100% {
                filter: drop-shadow(0 0 20px rgba(0, 255, 136, 0.5));
            }
            50% {
                filter: drop-shadow(0 0 40px rgba(0, 255, 136, 0.8));
            }
        }
        
        .status {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            background: rgba(0, 255, 136, 0.1);
            border: 2px solid #00ff88;
            padding: 16px 32px;
            border-radius: 50px;
            margin-top: 20px;
        }
        
        .pulse {
            width: 12px;
            height: 12px;
            background: #00ff88;
            border-radius: 50%;
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
                opacity: 1;
            }
            50% {
                transform: scale(1.5);
                opacity: 0.5;
            }
        }
        
        .status-text {
            color: #00ff88;
            font-size: 18px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        
        .subtitle {
            color: #666;
            font-size: 16px;
            margin-top: 20px;
            font-weight: 500;
        }
        
        /* Animated background grid */
        .grid {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0, 255, 136, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 136, 0.05) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: gridMove 20s linear infinite;
            z-index: 1;
        }
        
        @keyframes gridMove {
            0% {
                transform: translate(0, 0);
            }
            100% {
                transform: translate(50px, 50px);
            }
        }
        
        /* Floating particles */
        .particle {
            position: fixed;
            width: 4px;
            height: 4px;
            background: #00ff88;
            border-radius: 50%;
            opacity: 0;
            animation: float 8s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% {
                opacity: 0;
                transform: translateY(100vh) translateX(0);
            }
            10%, 90% {
                opacity: 0.6;
            }
            50% {
                transform: translateY(-100vh) translateX(100px);
            }
        }
        
        .particle:nth-child(1) { left: 10%; animation-delay: 0s; }
        .particle:nth-child(2) { left: 30%; animation-delay: 2s; }
        .particle:nth-child(3) { left: 50%; animation-delay: 4s; }
        .particle:nth-child(4) { left: 70%; animation-delay: 1s; }
        .particle:nth-child(5) { left: 90%; animation-delay: 3s; }
    </style>
</head>
<body>
    <div class="grid"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    
    <div class="container">
        <div class="logo">HUSTLISTAN</div>
        <div class="status">
            <div class="pulse"></div>
            <span class="status-text">Telegram API Server Online</span>
        </div>
        <div class="subtitle">2GB File Upload Capacity • Always Active</div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    """Branded landing page"""
    return render_template_string(LANDING_PAGE)

HEALTH_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Check - Hustlistan Telegram API</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #000000;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            text-align: center;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(0, 255, 136, 0.2);
            border-radius: 20px;
            padding: 60px;
            max-width: 600px;
        }
        .logo {
            font-size: 48px;
            font-weight: 900;
            background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 40px;
        }
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            padding: 20px 40px;
            border-radius: 50px;
            margin: 20px 0;
            font-size: 20px;
            font-weight: 600;
        }
        .status-healthy {
            background: rgba(0, 255, 136, 0.15);
            border: 2px solid #00ff88;
            color: #00ff88;
        }
        .status-initializing {
            background: rgba(255, 193, 7, 0.15);
            border: 2px solid #ffc107;
            color: #ffc107;
        }
        .pulse-healthy {
            width: 16px;
            height: 16px;
            background: #00ff88;
            border-radius: 50%;
            animation: pulse 1.5s ease-in-out infinite;
        }
        .pulse-warning {
            width: 16px;
            height: 16px;
            background: #ffc107;
            border-radius: 50%;
            animation: pulse 1.5s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.5); opacity: 0.5; }
        }
        .details {
            margin-top: 30px;
            color: #666;
            font-size: 14px;
            line-height: 1.8;
        }
        .detail-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        .detail-label { color: #888; }
        .detail-value { color: #00ff88; font-weight: 600; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">HUSTLISTAN</div>
        <div class="status-badge {{ status_class }}">
            <div class="{{ pulse_class }}"></div>
            <span>{{ status_text }}</span>
        </div>
        <div class="details">
            <div class="detail-row">
                <span class="detail-label">Bot API Status:</span>
                <span class="detail-value">{{ bot_status }}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Max Upload Size:</span>
                <span class="detail-value">2GB</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Endpoint:</span>
                <span class="detail-value">/health</span>
            </div>
        </div>
    </div>
</body>
</html>
"""

ERROR_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error - Hustlistan Telegram API</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #000000;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            text-align: center;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 68, 68, 0.3);
            border-radius: 20px;
            padding: 60px;
            max-width: 600px;
        }
        .logo {
            font-size: 48px;
            font-weight: 900;
            background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 30px;
        }
        .error-code {
            font-size: 72px;
            font-weight: 900;
            color: #ff4444;
            margin: 20px 0;
        }
        .error-message {
            color: #999;
            font-size: 18px;
            margin: 20px 0;
        }
        .note {
            background: rgba(255, 193, 7, 0.1);
            border: 1px solid rgba(255, 193, 7, 0.3);
            border-radius: 10px;
            padding: 20px;
            margin-top: 30px;
            color: #ffc107;
            font-size: 14px;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">HUSTLISTAN</div>
        <div class="error-code">{{ error_code }}</div>
        <div class="error-message">{{ error_message }}</div>
        <div class="note">
            <strong>⚠️ Note:</strong> {{ note }}
        </div>
    </div>
</body>
</html>
"""

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint with branded HTML page"""
    is_healthy = False
    bot_status = 'Initializing'
    
    try:
        # Check if Local Bot API is running
        response = requests.get(f'{LOCAL_API_URL}/bot{TELEGRAM_BOT_TOKEN}/getMe', timeout=5)
        if response.status_code == 200:
            is_healthy = True
            bot_status = 'Running'
    except:
        pass
    
    # Check if request wants JSON (for programmatic health checks)
    if request.headers.get('Accept') == 'application/json':
        if is_healthy:
            return {'status': 'healthy', 'bot_api': 'running'}, 200
        return {'status': 'starting', 'bot_api': 'initializing'}, 503
    
    # Return branded HTML page
    if is_healthy:
        html = HEALTH_PAGE_TEMPLATE.replace('{{ status_class }}', 'status-healthy')
        html = html.replace('{{ pulse_class }}', 'pulse-healthy')
        html = html.replace('{{ status_text }}', 'System Healthy')
        html = html.replace('{{ bot_status }}', 'Running')
        return html, 200
    else:
        html = HEALTH_PAGE_TEMPLATE.replace('{{ status_class }}', 'status-initializing')
        html = html.replace('{{ pulse_class }}', 'pulse-warning')
        html = html.replace('{{ status_text }}', 'Initializing')
        html = html.replace('{{ bot_status }}', 'Starting Up')
        return html, 503

@app.route('/bot<path:path>', methods=['GET', 'POST'])
def proxy_to_bot_api(path):
    """Proxy all /bot* requests to Local Bot API on port 8081"""
    try:
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
        
        # If it's a 404 and browser request, show branded error page
        if resp.status_code == 404 and 'text/html' in request.headers.get('Accept', ''):
            html = ERROR_PAGE_TEMPLATE.replace('{{ error_code }}', '404')
            html = html.replace('{{ error_message }}', 'Bot API Endpoint Not Found')
            html = html.replace('{{ note }}', 'The Telegram Bot API server is still initializing. This usually means the API credentials are invalid or the server is starting up. Check your TELEGRAM_API_ID and TELEGRAM_API_HASH environment variables.')
            return html, 404
        
        # Return the response as-is
        return Response(
            resp.content,
            status=resp.status_code,
            headers=dict(resp.headers)
        )
    except requests.exceptions.RequestException as e:
        # Connection error - Bot API not running
        if 'text/html' in request.headers.get('Accept', ''):
            html = ERROR_PAGE_TEMPLATE.replace('{{ error_code }}', '503')
            html = html.replace('{{ error_message }}', 'Bot API Server Unavailable')
            html = html.replace('{{ note }}', f'Cannot connect to Local Bot API server on port 8081. Error: {str(e)}')
            return html, 503
        return {'error': 'Bot API unavailable', 'details': str(e)}, 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
