# base image
FROM python:3.10-slim

# set working directory
WORKDIR /app

# install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# copy requirements
COPY requirements.txt .

# install python deps (with pip upgrade to avoid warnings)
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# copy app code
COPY . .

# default command
CMD ["python", "telegram_vc_userbot.py"]
