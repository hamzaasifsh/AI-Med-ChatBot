import requests

response = requests.post("http://127.0.0.1:8001/process-voice/")
print(response.json())  # Should print the transcribed text
