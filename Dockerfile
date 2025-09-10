FROM python:3.10-slim

WORKDIR /app

# -------- System dependencies install --------
RUN apt-get update && apt-get install -y \
    git \
    curl \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# -------- Try installing prebuilt PyAV wheel --------
# If no wheel is available, fallback to manual build with FFmpeg 4.3
RUN pip install --upgrade pip \
    && (pip install --no-cache-dir --only-binary=:all: av==8.1.0 || \
        (apt-get update && apt-get install -y \
            ffmpeg=7:4.3.6-0+deb11u1 \
            libavformat-dev=7:4.3.6-0+deb11u1 \
            libavcodec-dev=7:4.3.6-0+deb11u1 \
            libavdevice-dev=7:4.3.6-0+deb11u1 \
            libavutil-dev=7:4.3.6-0+deb11u1 \
            libswresample-dev=7:4.3.6-0+deb11u1 \
            libswscale-dev=7:4.3.6-0+deb11u1 \
            libavfilter-dev=7:4.3.6-0+deb11u1 \
            && rm -rf /var/lib/apt/lists/* \
        ) \
    )

# -------- Copy requirements and install --------
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# -------- Copy app code --------
COPY . .

# -------- Run app --------
CMD ["python", "telegram_vc_userbot.py"]
