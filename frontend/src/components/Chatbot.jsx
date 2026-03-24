import { useState } from "react";
import MessageBubble from "./MessageBubble";
import UploadImage from "./UploadImage";
import RecordAudio from "./RecordAudio";
import AudioPlayer from "./AudioPlayer";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [audioUrl, setAudioUrl] = useState(null);

  // ✅ Function to add a message to the chat
  const addMessage = (text, sender) => {
    setMessages((prev) => [...prev, { text, sender }]);
  };

  // ✅ Function to process user input (image/audio) and send it to the backend
  const processUserInput = async (imageFile, audioFile) => {
    const formData = new FormData();
    if (imageFile) formData.append("image", imageFile);
    if (audioFile) formData.append("audio", audioFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/process-patient/", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log("🔄 API Response:", data);  // ✅ Log response to debug

      // ✅ Display user's transcribed speech
      if (data.transcription) addMessage(data.transcription, "user");

      // ✅ Display AI Doctor's response (diagnosis)
      if (data.diagnosis) addMessage(data.diagnosis, "bot");

      // ✅ Play AI-generated speech
      if (data.audio_response) setAudioUrl(data.audio_response);
    } catch (error) {
      console.error("❌ Error processing input:", error);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* 🔹 Chat Header */}
      <div className="bg-blue-600 text-white text-lg font-semibold p-4 text-center">
        AI Healthcare Bot
      </div>

      {/* 🔹 Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((msg, index) => (
          <MessageBubble key={index} text={msg.text} sender={msg.sender} />
        ))}
      </div>

      {/* 🔹 Input Section (Upload Image, Record Audio, Play AI Speech) */}
      <div className="p-4 bg-white shadow-md flex items-center gap-2">
        <UploadImage onUpload={(image) => processUserInput(image, null)} />
        <RecordAudio onRecord={(audio) => processUserInput(null, audio)} />
        {audioUrl && <AudioPlayer audioUrl={audioUrl} />}
      </div>
    </div>
  );
};

export default Chatbot;
