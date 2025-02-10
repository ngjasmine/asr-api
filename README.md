# asr-api

Docker build
```
docker build --no-cache -t asr-api:v1 -f asr/Dockerfile .

```

Docker run
```
docker run -d --name asr-api -p 8001:8001 \
    -v $(pwd)/data/common_voice/cv-valid-dev:/mnt/cv-valid-dev \
    -v $(pwd)/data/common_voice/cv-valid-dev.csv:/mnt/cv-valid-dev.csv \
    asr-api:v1
```

Run cv-decode.py inside the API container:
```
docker exec -it asr-api python asr/cv-decode.py
```


Start FastAPI server
```
uvicorn asr.asr_api:app --host 0.0.0.0 --port 8001 --reload
```




```
python asr/cv-decode.py
```