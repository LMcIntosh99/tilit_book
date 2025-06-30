import React, { useState } from "react";
import axios from "axios";

type CommentFormProps = {
  onNewComment?: () => void;
};

const CommentForm = ({ onNewComment }: CommentFormProps) => {
  const [text, setText] = useState("");
  const [location, setLocation] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null;
    setFile(selectedFile);

    if (selectedFile) {
      const reader = new FileReader();
      reader.onload = () => setPreviewUrl(reader.result as string);
      reader.readAsDataURL(selectedFile);
    } else {
      setPreviewUrl(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setUploading(true);

    const formData = new FormData();
    formData.append("text", text);
    formData.append("location", location);
    if (file) formData.append("file", file);

    try {
      await axios.post("http://localhost:8000/comments", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      // Reset form
      setText("");
      setLocation("");
      setFile(null);
      setPreviewUrl(null);
      onNewComment?.();
    } catch (err) {
      console.error(err);
      alert("Error submitting comment");
    } finally {
      setUploading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-[#1e1e1e] text-white p-6 rounded-lg shadow-lg mb-8 max-w-2xl mx-auto"
    >
      <h2 className="text-2xl font-bold text-orange-500 mb-4">
        Have you seen Tilit?
      </h2>

      {previewUrl && (
        <img
          src={previewUrl}
          alt="Preview"
          className="mb-4 rounded-lg max-h-[400px] mx-auto"
        />
      )}

      <div className="flex flex-col gap-4">
        <input
          type="text"
          placeholder="Comment"
          value={text}
          onChange={(e) => setText(e.target.value)}
          required
          className="bg-black border border-gray-600 p-2 rounded text-white"
        />
        <input
          type="text"
          placeholder="Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          required
          className="bg-black border border-gray-600 p-2 rounded text-white"
        />
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="bg-black border border-gray-600 p-2 rounded text-white"
        />
        <button
          type="submit"
          disabled={uploading}
          className="bg-orange-600 hover:bg-orange-700 text-white font-semibold py-2 rounded disabled:opacity-50"
        >
          {uploading ? "Uploading..." : "Submit"}
        </button>
      </div>
    </form>
  );
};

export default CommentForm;
