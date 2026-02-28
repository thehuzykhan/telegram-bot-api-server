FROM ubuntu:22.04

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    gperf \
    zlib1g-dev \
    libssl-dev \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Clone and build Telegram Bot API
WORKDIR /app
RUN git clone --recursive https://github.com/tdlib/telegram-bot-api.git && \
    cd telegram-bot-api && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    cmake --build . --target install && \
    cd ../.. && \
    ls -la /usr/local/bin/

# Install Flask for health check endpoint
RUN pip3 install flask gunicorn requests

# Copy startup script
COPY start.sh /app/start.sh
COPY health_server.py /app/health_server.py
RUN chmod +x /app/start.sh

# Expose ports
EXPOSE 8081 10000

# Start both services
CMD ["/app/start.sh"]
