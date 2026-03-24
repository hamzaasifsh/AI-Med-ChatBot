import { useState } from "react";

const RecordAudio = ({ onRecord }) => {
  const [recording, setRecording] = useState(false);
  let mediaRecorder;
  let audioChunks = [];

  const startRecording = async () => {
    setRecording(true);
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
      onRecord(audioBlob); // ✅ Send audio to chatbot
      setRecording(false);
    };

    setTimeout(() => {
      mediaRecorder.stop();
    }, 5000); // Auto-stop after 5 seconds
  };

  return (
    <button onClick={startRecording} className="bg-green-500 text-white px-4 py-2 rounded">
      {recording ? "Recording..." : "Record Voice"}
    </button>
  );
};

export default RecordAudio;
