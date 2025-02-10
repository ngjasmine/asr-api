from pathlib import Path
import os
import pandas as pd
import requests

# Paths
project_root = Path().resolve()
cv_valid_dev_path = project_root / "data" / "common_voice" / "cv-valid-dev"
cv_valid_dev_csv = project_root / "data" / "common_voice" / "cv-valid-dev.csv"
updated_csv = project_root / "data" / "cv-valid-dev-updated.csv"

# Load the csv path
df = pd.read_csv(str(cv_valid_dev_csv))

# Select first 10 files for test
df = df.iloc[:10]

# FastAPI URL
api_url = "http://localhost:8001/asr"

# Obtain audio files in folder
# requests expected format is: ("files", (filename, open(filename, "rb"), "audio/mpeg"))
audio_files = [
    ("files", (filename, open(str(cv_valid_dev_path / filename), "rb"), "audio/mpeg"))
    for filename in df["filename"] if os.path.exists(str(cv_valid_dev_path / filename))
]

# Send the request
response = requests.post(api_url, files=audio_files)

if response.status_code == 200:
    transcriptions = response.json()

else:
    print(f"Error: {response.text}")
    transcriptions = {}

# Close opened files
for _, file_tuple in audio_files:
    file_tuple[1].close()

# Map transcriptions to df  
df["generated_text"] = df["filename"].map(lambda x: transcriptions.get(x, {}).get("transcription", ""))

# Save updated CSV
df.to_csv(str(cv_valid_dev_csv), index=False)
print(f"Updated CSV saved at {str(cv_valid_dev_csv)}")