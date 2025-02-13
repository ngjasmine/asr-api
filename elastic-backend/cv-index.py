import csv
import os
from elasticsearch import Elasticsearch, helpers
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve the Elasticsearch credentials from environment variables
ELASTIC_ENDPOINT = os.getenv("ELASTIC_ENDPOINT")
ELASTIC_API_KEY_ID = os.getenv("ELASTIC_API_KEY_ID")
ELASTIC_API_KEY_SECRET = os.getenv("ELASTIC_API_KEY_SECRET")

# # Configure  Elastic cloud
# es = Elasticsearch(
#     hosts=[ELASTIC_ENDPOINT],
#     api_key=(ELASTIC_API_KEY_ID, ELASTIC_API_KEY_SECRET)
# )

# Configure Elasticsearch for local dev
# es = Elasticsearch("http://localhost:9200")

# Configure Elasticsearch for AWS deployment
es = Elasticsearch("http://elasticsearch-node1:9200")

index_name = "cv-transcriptions"

index_body = {
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "filename": { "type": "text" },
            "text": { "type": "text" },
            "generated_text": {
                "type": "text",
                "fields": {
                    "suggest": {
                        "type": "search_as_you_type",
                        "doc_values": False,
                        "max_shingle_size": 3,
                        "store": True
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
}

def delete_index(index_name):
    """Deletes the index if it exists."""
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        print(f"Index '{index_name}' deleted successfully.")

def create_index(index_name, index_body):
    """Creates the index with the given settings and mappings."""
    response = es.indices.create(index=index_name, body=index_body)
    print(f"Index '{index_name}' created successfully.")
    print(response)

def csv_to_actions(csv_file, index_name):
    """Generator function that reads CSV rows and yields actions for bulk indexing."""
    with open(csv_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print("Indexing row:", row)

            # For each field, if it's blank, assign a default empty string (or a default value if desired), not undefined or null
            row["filename"] = row.get("filename", "").strip()
            row["text"] = row.get("text", "").strip()
            row["generated_text"] = row.get("generated_text", "").strip()
            # For numeric fields, assign default 0 if blank
            row["up_votes"] = int(row["up_votes"]) if row.get("up_votes", "").strip() else 0
            row["down_votes"] = int(row["down_votes"]) if row.get("down_votes", "").strip() else 0
            row["duration"] = float(row["duration"]) if row.get("duration", "").strip() else 0.0
            # For keyword fields, assign an empty string if blank
            row["age"] = row.get("age", "").strip()
            row["gender"] = row.get("gender", "").strip()
            row["accent"] = row.get("accent", "").strip()


            # Optionally convert fields as needed (e.g., numbers, empty strings, etc.)
            # For example, if up_votes/down_votes should be integers:
            row["up_votes"] = int(row["up_votes"]) if row["up_votes"] else 0
            row["down_votes"] = int(row["down_votes"]) if row["down_votes"] else 0
            row["duration"] = float(row["duration"]) if row["duration"] else 0.0

            yield {
                "_index": index_name,
                "_source": row,
            }

if __name__ == "__main__":
    # csv_file = "data/common_voice/cv-valid-dev.csv" 
    csv_file = "/app/cv-valid-dev.csv"
    
    # Delete index if it exists
    delete_index(index_name)

    # Create a fresh index
    create_index(index_name, index_body)
    
    # Use the bulk helper to index all documents
    helpers.bulk(es, csv_to_actions(csv_file, index_name))
    print("Bulk indexing completed.")