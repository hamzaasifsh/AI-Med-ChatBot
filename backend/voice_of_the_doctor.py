from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
import os
import platform
import subprocess
from dotenv import load_dotenv
import elevenlabs
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment

# Load environment variables
load_dotenv()

# Retrieve API Key for ElevenLabs
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise ValueError("❌ ELEVENLABS_API_KEY is missing! Please check your .env file.")

# Initialize FastAPI app
app = FastAPI()

# Audio file storage directory
os.makedirs("generated_audio", exist_ok=True)

# ✅ Convert Text to Speech using ElevenLabs API
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

        # ✅ Print AI Doctor's response for debugging
        print(f"📝 AI Doctor's Response: {input_text}")

        # Generate speech and save as MP3
        audio = client.generate(
            text=input_text,
            voice="Aria",
            output_format="mp3_22050_32",
            model="eleven_turbo_v2"
        )

        # Save the generated audio
        with open(output_filepath, "wb") as f:
            f.write(b"".join(audio))

        # Convert MP3 to WAV for Windows playback
        output_wav_filepath = output_filepath.replace(".mp3", ".wav")
        audio_segment = AudioSegment.from_mp3(output_filepath)
        audio_segment.export(output_wav_filepath, format="wav")

        # Auto-play the generated audio
        play_audio(output_filepath)

        return output_filepath
    except Exception as e:
        print(f"❌ Error generating speech with ElevenLabs: {e}")
        return None

# ✅ Function to Auto-Play Audio on Different OS
def play_audio(file_path):
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', file_path])
        elif os_name == "Windows":  # Windows requires WAV format
            wav_file = file_path.replace(".mp3", ".wav")
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_file}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', file_path])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"❌ Error playing audio: {e}")

# ✅ FastAPI Endpoint for ElevenLabs TTS
@app.post("/text-to-speech/elevenlabs/")
async def generate_speech_elevenlabs(text: str = Form(...)):
    """
    Converts input text into speech using ElevenLabs API and returns AI response (text + audio).
    """
    print(f"🔹 Received Text for TTS: {text}")  # ✅ Print input text

    output_filepath = f"generated_audio/elevenlabs_output.mp3"
    generated_audio = text_to_speech_with_elevenlabs(text, output_filepath)

    if not generated_audio:
        return JSONResponse(content={"error": "Text-to-Speech generation failed."}, status_code=500)

    print(f"✅ Speech generated: {output_filepath}")  # ✅ Print generated file path

    # ✅ Return both the AI diagnosis text & the audio file URL
    return JSONResponse(
        content={
            "ai_response": text,  # ✅ AI Doctor's response
            "audio_url": f"http://127.0.0.1:8003/generated_audio/elevenlabs_output.mp3"  # ✅ Speech file URL
        }
    )
