import pandas as pd
import numpy as np
from elasticsearch import Elasticsearch, helpers

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Load CSV
# csv_file = "/usr/share/elasticsearch/cv-valid-dev.csv"
csv_file = "data/common_voice/cv-valid-dev.csv"
df = pd.read_csv(csv_file)

# Replace NaN values with None (which becomes null in JSON)
df = df.replace({np.nan: None})

# Define Elasticsearch index
index_name = "cv-transcriptions"

# Delete existing index (if needed)
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# Define mappings for correct data types
mappings = {
    "mappings": {
        "properties": {
            "filename": {"type": "text"},
            "text": {"type": "text"},
            "generated_text": {"type": "text"},
            "age": {"type": "keyword"},
            "gender": {"type": "keyword"},
            "accent": {"type": "keyword"},
            "duration": {"type": "float"},
            "up_votes": {"type": "integer"},
            "down_votes": {"type": "integer"}
        }
    }
}

# Create index with mappings
es.options(ignore_status=400).indices.create(index=index_name, body=mappings)

# Prepare data for bulk indexing
def generate_data():
    for _, row in df.iterrows():
        yield {
            "_index": index_name,
            "_source": row.to_dict()
        }

# Bulk index data
helpers.bulk(es, generate_data())

print(f"Successfully indexed {len(df)} records into {index_name}")