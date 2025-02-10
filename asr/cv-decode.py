from pathlib import Path
import os
import pandas as pd
import requests

# # Paths (local dev)
# project_root = Path().resolve()
# cv_valid_dev_path = project_root / "data" / "common_voice" / "cv-valid-dev"
# cv_valid_dev_csv = project_root / "data" / "common_voice" / "cv-valid-dev.csv"

# Path (docker)
cv_valid_dev_csv = Path("/mnt/cv-valid-dev.csv")

# Vol mount (docker)
cv_valid_dev_path = Path("/mnt/cv-valid-dev")

# Load the csv path
df = pd.read_csv(str(cv_valid_dev_csv))

# # Get smaller subset for test
# df =df.iloc[:38]

# Ensure "generated_text" column exists
if "generated_text" not in df.columns:
    df["generated_text"] = ""

# FastAPI URL
api_url = "http://localhost:8001/asr"

# send 1 file per request and del each file aft processing
for index, row in df.iterrows():
    file_path = cv_valid_dev_path / row["filename"]
    
    if not file_path.exists():
        print(f"Skipping {file_path}, file not found.")
        continue

    # Open file and send request
    with open(file_path, "rb") as audio_file:
        response = requests.post(api_url, files={"file": (row["filename"], audio_file, "audio/mpeg")})

    if response.status_code == 200:
        transcription = response.json()
        print(f"Processing: {file_path}")
        print(f"API Response: {response.status_code} - {response.text}") 
        filename_key = row["filename"]
        df.at[index, "generated_text"] = transcription[filename_key].get("transcription", "")

        # Delete file after successful processing
        os.remove(file_path)
        print(f"Processed & deleted: {file_path}")

    else:
        print(f"Failed to process {file_path}, API error: {response.status_code}")

# Save updated csv
df.to_csv(cv_valid_dev_csv, index=False) 
print(f"Updated CSV saved at {cv_valid_dev_csv}")

# BELOW CODE FOR RUNNING LOCALLY #
# # Obtain audio files in folder
# # requests expected format is: ("files", (filename, open(filename, "rb"), "audio/mpeg"))
# audio_files = [
#     ("files", (filename, open(str(cv_valid_dev_path / filename), "rb"), "audio/mpeg"))
#     for filename in df["filename"] if os.path.exists(str(cv_valid_dev_path / filename))
# ]

# # Send the request
# response = requests.post(api_url, files=audio_files)

# if response.status_code == 200:
#     transcriptions = response.json()
#     # Delete the file after successful processing
#     os.remove(file_path)
#     print(f"Processed & deleted: {file_path}")
    
# else:
#     print(f"Error: {response.text}")
#     transcriptions = {}

# # Close opened files
# for _, file_tuple in audio_files:
#     file_tuple[1].close()

# # Map transcriptions to df  
# df["generated_text"] = df["filename"].map(lambda x: transcriptions.get(x, {}).get("transcription", ""))

# # Save updated CSV
# df.to_csv(str(cv_valid_dev_csv), index=False)
# print(f"Updated CSV saved at {str(cv_valid_dev_csv)}")