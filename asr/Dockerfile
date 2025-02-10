FROM python:3.11-slim

WORKDIR /asr-api

# Install system dependencies (including FFmpeg)
RUN apt-get update && \ 
    apt-get install -y ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*
    
COPY ../requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "asr.asr_api:app", "--host", "0.0.0.0", "--port", "8001"]