FROM python:3.10-slim
WORKDIR /app
COPY . /app
# Install ffmpeg with NVENC support and HandBrakeCLI
RUN apt-get update && \
    apt-get install -y ffmpeg handbrake-cli procps && \
    pip install --no-cache-dir -r requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
