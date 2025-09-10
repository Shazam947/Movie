FROM python:3.10-slim

WORKDIR /app

# -------- System dependencies install --------
RUN apt-get update && apt-get install -y \
    git \
    curl \
    pkg-config \
    build-essential \
    ffmpeg \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libswresample-dev \
    libswscale-dev \
    libavfilter-dev \
    && rm -rf /var/lib/apt/lists/*

# -------- Install Python dependencies --------
COPY requirements.txt .

RUN pip install --upgrade pip \
    && (pip install --no-cache-dir --only-binary=:all: av==8.1.0 || pip install --no-cache-dir av==8.1.0) \
    && pip install --no-cache-dir -r requirements.txt

# -------- Copy app code --------
COPY . .

# -------- Run app --------
CMD ["python", "telegram_vc_userbot.py"]
