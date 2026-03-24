import { useEffect, useRef } from "react";

const AudioPlayer = ({ audioUrl }) => {
  const audioRef = useRef(null);

  useEffect(() => {
    if (audioUrl && audioRef.current) {
      audioRef.current.play().catch((error) => {
        console.error("🔴 Error playing audio:", error);
      });
    }
  }, [audioUrl]);

  return (
    <div className="mt-2">
      {audioUrl && (
        <audio ref={audioRef} controls autoPlay>
          <source src={audioUrl} type="audio/mpeg" />
          Your browser does not support the audio element.
        </audio>
      )}
    </div>
  );
};

export default AudioPlayer;
