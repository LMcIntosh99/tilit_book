import React, { useState } from "react";
import axios from "axios";

const CommentForm = () => {
  const [text, setText] = useState("");
  const [location, setLocation] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  const formData = new FormData();
  formData.append("text", text);
  formData.append("location", location);
  if (file) {
    console.log("filee")
    formData.append("file", file);
    console.log(file)
  }

  try {
    await axios.post("http://localhost:8000/comments", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    // Reset form
    setText("");
    setLocation("");
    setFile(null);
    alert("Comment submitted!");
  } catch (err) {
    console.error(err);
    alert("Error submitting comment");
  }
};


    return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 max-w-md mx-auto">
      <input
        type="text"
        placeholder="Comment"
        value={text}
        onChange={(e) => setText(e.target.value)}
        required
        className="border p-2 rounded"
      />
      <input
        type="text"
        placeholder="Location"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        required
        className="border p-2 rounded"
      />
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="border p-2 rounded"
      />
      <button
        type="submit"
        disabled={uploading}
        className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {uploading ? "Uploading..." : "Submit"}
      </button>
    </form>
  );
};

export default CommentForm;
