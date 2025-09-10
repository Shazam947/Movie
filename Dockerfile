# Base image
FROM python:3.10-slim

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system deps (ffmpeg + dev libs for PyAV)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavutil-dev \
    libswresample-dev \
    libswscale-dev \
    gcc \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working dir
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python deps
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (agar bot ka web server use kare)
EXPOSE 8080

# Run bot
CMD ["python", "main.py"]
