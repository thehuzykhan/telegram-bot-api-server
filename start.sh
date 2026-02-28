#!/bin/bash

# Start Telegram Bot API in background
echo "Starting Telegram Bot API..."
/usr/local/bin/telegram-bot-api \
    --api-id=${TELEGRAM_API_ID} \
    --api-hash=${TELEGRAM_API_HASH} \
    --local \
    --http-port=8081 &

# Wait for it to initialize
echo "Waiting for Bot API to start..."
sleep 10

# Start health check server on port 10000 (Render's default)
echo "Starting health check server..."
exec gunicorn -b 0.0.0.0:10000 health_server:app
