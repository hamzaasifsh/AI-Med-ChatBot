from fastapi import FastAPI
import logging
import os
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Retrieve API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is missing! Please check your .env file.")

# Initialize FastAPI app
app = FastAPI()

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Whisper AI Model
STT_MODEL = "whisper-large-v3"


# Step 1: Record Audio from Microphone
def record_audio():
    """
    Records audio from the microphone and saves it as an MP3 file.
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("🎤 Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("🎤 Start speaking now...")

            # Record the audio
            audio_data = recognizer.listen(source, timeout=20, phrase_time_limit=None)
            logging.info("🎤 Recording complete.")

            # Convert the recorded audio to an MP3 file
            os.makedirs("recordings", exist_ok=True)
            file_path = "recordings/patient_voice.mp3"

            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")

            logging.info(f"✅ Audio saved to {file_path}")
            return file_path  # ✅ Return file path for further processing

    except Exception as e:
        logging.error(f"❌ An error occurred: {e}")
        return None  # Return None in case of an error


# Step 2: Transcribe Recorded Speech to Text
def transcribe_with_groq(audio_filepath):
    """
    Transcribes recorded speech to text using GROQ Whisper AI.
    """
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=STT_MODEL,
                file=audio_file,
                language="en"
            )

        return transcription.text

    except Exception as e:
        logging.error(f"❌ Transcription error: {e}")
        return None


# Step 3: FastAPI Endpoint for Voice Processing
@app.post("/process-voice/")
async def process_voice():
    """
    Records user's voice, transcribes it using Whisper AI, and returns the text.
    """
    # Record user voice
    audio_path = record_audio()
    if not audio_path:
        return {"error": "Failed to record audio"}

    # Transcribe the recorded voice
    transcription = transcribe_with_groq(audio_path)
    if not transcription:
        return {"error": "Failed to transcribe audio"}

    return {"transcription": transcription}
