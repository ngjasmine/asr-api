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


Task 3

Ensure Docker daemon is running, then run docker compose
```
docker compose -f deployment-design/docker-compose.yml up -d
```

Use curl to bulk index the data
```
docker exec -i elasticsearch curl -X POST "http://localhost:9200/_bulk" \
  -H "Content-Type: application/json" \
  --data-binary "@/usr/share/elasticsearch/data.json"
```

## For local development
fork and clone this repository

Setup Instructions
- **Windows users:** Run `setup.bat`
- **macOS/Linux users:** Run `setup.sh`


```
cd deployment-design
docker compose up -d elasticsearch-node1 elasticsearch-node2
```

check both nodes running
```
docker ps
```

CREATE INDEX
```
curl -X PUT "http://localhost:9200/cv-transcriptions" -H "Content-Type: application/json" -d '{
  "settings": { "number_of_shards": 2, "number_of_replicas": 1 },
  "mappings": {
    "properties": {
      "filename": { "type": "text" },
      "text": { "type": "text" },
      "generated_text": {
        "type": "text",
        "fields": {
          "suggest": {
            "type": "search_as_you_type",
            "doc_values": false,
            "max_shingle_size": 3,
            "store": true
          }
        }
      },
      "age": { "type": "keyword" },
      "gender": { "type": "keyword" },
      "accent": { "type": "keyword" },
      "duration": { "type": "float" },
      "up_votes": { "type": "integer" },
      "down_votes": { "type": "integer" }
    }
  }
}'

```

IF DATA WRONGLY INDEXE, or alr exists but in a wrong format, DELETE IT FIRST
```
curl -X DELETE "http://localhost:9200/cv-transcriptions"
```

RUN INDEXING
```
cd ..
python elastic-backend/cv-index.py
```


Check if data is indexed and searchable
```
curl -X GET "http://localhost:9200/cv-transcriptions/_search?pretty"
```
Check mapping is correct
```
curl -X GET "http://localhost:9200/cv-transcriptions/_mapping?pretty"
```

Start Search UI
```
cd deployment-design
docker compose up -d search-ui
```

To visit search UI, open a browser and go to http://localhost:3000

