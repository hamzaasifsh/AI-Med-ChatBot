# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#Step1a: Setup Text to Speech–TTS–model with gTTS
import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)


# input_text="Hi this is Ai with Hassan!"
# text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")

#Step1b: Setup Text to Speech–TTS–model with ElevenLabs
import elevenlabs
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.generate(
        text= input_text,
        voice= "Aria",
        output_format= "mp3_22050_32",
        model= "eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)

# input_text="Hi this is Ai with Hassan!"
# text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3") 

# Step2: Use Model for Text output to Voice

import os
import platform
import subprocess
from gtts import gTTS
from pydub import AudioSegment

def text_to_speech_with_gtts(input_text, output_mp3_filepath):
    language = "en"

    # Generate MP3 file from gTTS
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_mp3_filepath)
    # print(f"✅ MP3 audio file saved as: {output_mp3_filepath}")

    # Convert MP3 to WAV for Windows playback
    output_wav_filepath = output_mp3_filepath.replace(".mp3", ".wav")
    audio = AudioSegment.from_mp3(output_mp3_filepath)
    audio.export(output_wav_filepath, format="wav")
    # print(f"✅ Converted to WAV: {output_wav_filepath}")

    # Detect OS and play audio
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_mp3_filepath])
        elif os_name == "Windows":  # Windows requires WAV format
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_wav_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_mp3_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"❌ An error occurred while playing the audio: {e}")

# # ✅ Test the function
# input_text = "Hi, this is AI with Hassan, autoplay testing!"
# text_to_speech_with_gtts(input_text=input_text, output_mp3_filepath="gtts_testing_autoplay.mp3")



import os
import platform
import subprocess
import elevenlabs
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment

# Ensure your API key is loaded correctly
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_elevenlabs(input_text, output_filepath="final.mp3"):
    """
    Converts text to speech using ElevenLabs API and saves it to the specified file.
    """
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    

    # Generate speech and save as MP3
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )

    # ✅ Convert the generator to raw bytes
    audio_bytes = b"".join(audio)

    with open(output_filepath, "wb") as f:
        f.write(audio_bytes)  # ✅ This now correctly writes the file

    print(f"✅ ElevenLabs MP3 audio saved: {output_filepath}")

    # Convert MP3 to WAV for Windows playback
    output_wav_filepath = output_filepath.replace(".mp3", ".wav")
    audio_segment = AudioSegment.from_mp3(output_filepath)
    audio_segment.export(output_wav_filepath, format="wav")
    print(f"✅ Converted to WAV: {output_wav_filepath}")

    # Detect OS and play audio
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows requires WAV format
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_wav_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"❌ Error playing audio: {e}")

    return output_filepath  # ✅ Return file path for Gradio

# # ✅ Test the function
# input_text = "Hello, this is ElevenLabs TTS with autoplay!"
# text_to_speech_with_elevenlabs(input_text, output_mp3_filepath="elevenlabs_testing_autoplay.mp3")


