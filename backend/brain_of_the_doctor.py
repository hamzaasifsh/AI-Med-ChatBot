from fastapi import FastAPI, UploadFile, File
import os
import base64
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Retrieve API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is missing! Please check your .env file.")

# FastAPI app instance
app = FastAPI()

# Model to use
MODEL_NAME = "llama-3.2-90b-vision-preview"

# Step 1: Convert Image to Base64 Format
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

# Step 2: Analyze Image Using GROQ's AI Model
def analyze_image_with_query(query, encoded_image):
    client = Groq(api_key=GROQ_API_KEY)

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}},
            ],
        }
    ]

    chat_completion = client.chat.completions.create(messages=messages, model=MODEL_NAME)
    return chat_completion.choices[0].message.content

# Step 3: FastAPI Endpoint to Process Images
@app.post("/analyze-image/")
async def analyze_image(image: UploadFile = File(...)):
    """
    Receives an image, encodes it, sends it to GROQ AI, and returns a medical diagnosis.
    """
    try:
        # Convert image to Base64
        encoded_image = encode_image(image.file)

        # Medical Query for AI Analysis
        query = "Is there something wrong with my face? Provide a short medical diagnosis."

        # Analyze Image
        diagnosis = analyze_image_with_query(query, encoded_image)

        return {"diagnosis": diagnosis}

    except Exception as e:
        return {"error": str(e)}
