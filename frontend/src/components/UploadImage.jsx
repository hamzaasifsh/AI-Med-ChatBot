import { useState } from "react";

const UploadImage = ({ onUpload }) => {
  const [image, setImage] = useState(null);

  const handleImageChange = (event) => {
    setImage(event.target.files[0]);
  };

  const handleUpload = () => {
    if (!image) return alert("Please select an image.");
    onUpload(image); // ✅ Send image to chatbot
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleImageChange} />
      <button onClick={handleUpload} className="bg-blue-500 text-white px-4 py-2 rounded">
        Upload Image
      </button>
    </div>
  );
};

export default UploadImage;
