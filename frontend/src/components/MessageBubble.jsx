const MessageBubble = ({ text, sender }) => {
    const isUser = sender === "user";
  
    return (
      <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-2`}>
        <div
          className={`p-3 rounded-lg max-w-[70%] ${
            isUser ? "bg-blue-500 text-white" : "bg-gray-300 text-black"
          }`}
        >
          {text}
        </div>
      </div>
    );
  };
  
  export default MessageBubble;
  