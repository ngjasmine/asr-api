from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
from fastapi import FastAPI, File, UploadFile
import numpy as np
import io
from pydub import AudioSegment
from typing import List

app = FastAPI()

# load model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

@app.get("/ping")
def ping():
    """
    Check if service is working.
    """
    return{"message": "pong"}

@app.post("/asr")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    ASR endpoint that transcribes multiple MP3 files.
    """
    response = {}

    # Read uploaded file
    audio_data = await file.read()

    # Convert MP3 to WAV (16kHz, mono)
    audio = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
    audio = audio.set_frame_rate(16000).set_channels(1)

    # Convert to NumPy array
    samples = np.array(audio.get_array_of_samples(), dtype=np.float32) / 32768.0  # Normalize

    # Process input
    input_values = processor(samples, return_tensors="pt", sampling_rate=16000).input_values

    # Perform inference
    with torch.no_grad():
        logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)

    # Decode transcription
    transcription = processor.batch_decode(predicted_ids)[0]

    # Calculate duration
    duration = str(round(len(audio) / 1000, 2))  # Duration in seconds (milliseconds to seconds), to 2 dp

    # append file's result to response dictionary
    response[file.filename] = {
        "transcription": transcription, 
        "duration": duration
        }

    return response