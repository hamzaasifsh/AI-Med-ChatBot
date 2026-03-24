from fastapi import FastAPI, File, UploadFile, HTTPException
import requests
import os
from fastapi.responses import JSONResponse

app = FastAPI()

# Microservice URLs
VOICE_SERVICE_URL = "http://127.0.0.1:8001/process-voice/"
IMAGE_SERVICE_URL = "http://127.0.0.1:8002/analyze-image/"
TTS_SERVICE_URL = "http://127.0.0.1:8003/text-to-speech/elevenlabs/"

# ✅ Step 1: Process Patient's Voice
def get_transcription():
    try:
        print("🔄 Sending request to voice processing API...")
        response = requests.post(VOICE_SERVICE_URL)
        response.raise_for_status()
        transcription = response.json().get("transcription", "")
        print(f"✅ Voice Transcription: {transcription}")
        return transcription
    except requests.exceptions.RequestException as e:
        return f"❌ Error in voice processing: {e}"

# ✅ Step 2: Analyze Image
def analyze_image(image: UploadFile):
    try:
        print("🔄 Sending request to image processing API...")
        files = {"image": (image.filename, image.file, image.content_type)}
        response = requests.post(IMAGE_SERVICE_URL, files=files)
        response.raise_for_status()
        diagnosis = response.json().get("diagnosis", "")
        print(f"✅ Image Analysis: {diagnosis}")
        return diagnosis
    except requests.exceptions.RequestException as e:
        return f"❌ Error in image analysis: {e}"

# ✅ Step 3: Convert AI Diagnosis to Speech
def generate_speech(text):
    try:
        print("🔄 Sending request to text-to-speech API...")
        data = {"text": text}
        response = requests.post(TTS_SERVICE_URL, data=data)
        response.raise_for_status()

        # ✅ Ensure API response has `audio_url`
        tts_response = response.json()
        audio_url = tts_response.get("audio_response")  # ✅ Change from audio_path to audio_response
        print(f"✅ TTS Audio URL: {audio_url}")
        return audio_url
    except requests.exceptions.RequestException as e:
        print(f"❌ Error in text-to-speech: {e}")
        return None  # ✅ Return None if TTS fails

# ✅ Step 4: Main API Endpoint
@app.post("/process-patient/")
async def process_patient(image: UploadFile = File(...)):
    """
    1️⃣ Records user's voice & transcribes it.
    2️⃣ Analyzes the provided image.
    3️⃣ Generates AI diagnosis.
    4️⃣ Converts diagnosis to speech.
    5️⃣ Returns transcription, diagnosis, and audio file.
    """
    # ✅ Step 1: Get transcription
    transcription = get_transcription()
    if "❌" in transcription:
        return JSONResponse(content={"error": "Voice processing failed", "transcription": None}, status_code=500)

    # ✅ Step 2: Analyze Image
    diagnosis = analyze_image(image)
    if "❌" in diagnosis:
        return JSONResponse(content={"error": "Image analysis failed", "diagnosis": None}, status_code=500)

    # ✅ Step 3: Convert AI Diagnosis to Speech
    audio_url = generate_speech(diagnosis)
    if not audio_url:
        print("❌ TTS Failed: Returning diagnosis without audio.")
        return JSONResponse(
            content={
                "transcription": transcription,
                "diagnosis": diagnosis,
                "audio_response": None
            },
            status_code=200
        )

    # ✅ Return full AI response (Text + Speech)
    return JSONResponse(
        content={
            "transcription": transcription,
            "diagnosis": diagnosis,
            "audio_response": audio_url
        },
        status_code=200
    )
