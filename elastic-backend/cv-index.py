import pandas as pd
import json
import numpy as np

# Load CSV
csv_file = "../data/common_voice/cv-valid-dev.csv" 
df = pd.read_csv(csv_file)

# Replace NaN values with None (which becomes null in JSON)
df = df.replace({np.nan: None})

# Convert to Elasticsearch-friendly JSON format
records = []
for i, row in df.iterrows():
    record = {
        "_index": "search-index",
        "_id": i,
        "_source": row.to_dict()
    }
    records.append(record)

# Save to JSON
json_file = "data.json"

# NDJSON format: used for bulk indexing
with open(json_file, "w") as f:
    for i, row in df.iterrows():
        # Write the metadata line first
        f.write(json.dumps({"index": {"_index": "search-index", "_id": i + 1}}) + "\n")
        # Write the actual document
        f.write(json.dumps(row.to_dict()) + "\n")

print(f"JSON file saved: {json_file}")