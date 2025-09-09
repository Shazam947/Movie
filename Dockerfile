FROM python:3.10-slim


# install ffmpeg + build deps
RUN apt-get update && apt-get install -y ffmpeg build-essential libssl-dev libffi-dev && rm -rf /var/lib/apt/lists/*


WORKDIR /app


# copy repo files
COPY . /app


# install python deps
RUN pip install --no-cache-dir -r requirements.txt


ENV TEMP_DIR=/tmp/vc_userbot


CMD ["python", "telegram_vc_userbot.py"]
