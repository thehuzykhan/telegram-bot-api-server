# Telegram Local Bot API Server

This is a self-hosted Telegram Bot API server that enables 2GB file uploads for Hustlistan course videos.

## Deployment Instructions

### 1. Create New GitHub Repository

```bash
# Create a new repo on GitHub called "telegram-bot-api-server"
# Then push these files:
cd telegram-bot-api-server
git init
git add .
git commit -m "Initial commit: Telegram Local Bot API server"
git remote add origin https://github.com/YOUR_USERNAME/telegram-bot-api-server.git
git push -u origin main
```

### 2. Deploy to Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New** → **Web Service**
3. Connect your GitHub repository
4. Render will auto-detect the `render.yaml` configuration
5. Add these **Environment Variables**:
   - `TELEGRAM_API_ID` = Your API ID from https://my.telegram.org
   - `TELEGRAM_API_HASH` = Your API Hash from https://my.telegram.org
   - `TELEGRAM_BOT_TOKEN` = Your existing bot token
6. Click **Create Web Service**

### 3. Wait for Build

- Build takes ~8-12 minutes (compiling C++)
- Watch logs for "Starting health check server..."
- Once healthy, copy your URL (e.g., `https://hustlistan-telegram-api.onrender.com`)

### 4. Update Main App

Add this to your main app's `.env` file:
```
TELEGRAM_API_BASE=https://YOUR-RENDER-URL.onrender.com
```

Then update your main `app.py` to use this endpoint instead of `https://api.telegram.org`

## Testing

Once deployed, test with:
```bash
curl https://YOUR-RENDER-URL.onrender.com/health
```

Should return:
```json
{"status": "healthy", "bot_api": "running"}
```

## Features

- **2GB file upload limit** (vs 50MB on standard API)
- **Free tier compatible** with keep-alive pings
- **Health check endpoint** at `/health`
- **Automatic proxy** to Local Bot API on port 8081

## Architecture

```
Your Main App (app.py)
    ↓ HTTPS
Health Server (port 10000)
    ↓ HTTP
Local Bot API (port 8081)
    ↓
Telegram Servers
```
