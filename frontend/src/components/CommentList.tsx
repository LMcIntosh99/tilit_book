import { useEffect, useState } from "react";
import axios from "axios";
import { type Comment } from "../types";

const CommentList = () => {
  const [comments, setComments] = useState<Comment[]>([]);
  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  useEffect(() => {
    axios.get("http://localhost:8000/comments")
      .then(res => setComments(res.data))
      .catch(err => console.error("Failed to load comments", err));
  }, []);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString("en-GB", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  return (
    <div style={{ padding: "1rem", maxWidth: "600px", margin: "0 auto" }}>
      <h3 style={{ color: "orange" }}>Comments</h3>
      {Array.isArray(comments) ? comments.map((c) => (
        <div
          key={c.id}
          style={{
            backgroundColor: "#1e1e1e",
            padding: "1rem",
            marginBottom: "1.5rem",
            borderRadius: "12px",
            boxShadow: "0 2px 10px rgba(0,0,0,0.5)",
          }}
        >
          <p style={{ color: "#eee", marginBottom: "0.5rem" }}>{c.text}</p>
          <small style={{ color: "orange", display: "block", marginBottom: "0.5rem" }}>
            {c.location} – {formatDate(c.created_at)}
          </small>
          {c.image_url && (
            <img
              src={c.image_url}
              alt="Cat"
              onClick={() => setSelectedImage(c.image_url)}
              style={{
                maxWidth: "100%",
                borderRadius: "8px",
                cursor: "pointer",
                transition: "transform 0.2s",
              }}
              onMouseOver={e => (e.currentTarget.style.transform = "scale(1.02)")}
              onMouseOut={e => (e.currentTarget.style.transform = "scale(1)")}
            />
          )}
        </div>
      )) : <p>Loading comments...</p>}

      {selectedImage && (
        <div
          onClick={() => setSelectedImage(null)}
          style={{
            position: "fixed",
            top: 0, left: 0,
            width: "100vw", height: "100vh",
            backgroundColor: "rgba(0, 0, 0, 0.85)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 1000,
          }}
        >
          <button
            onClick={(e) => {
              e.stopPropagation();
              setSelectedImage(null);
            }}
            style={{
              position: "absolute",
              top: "20px",
              right: "30px",
              background: "transparent",
              color: "white",
              border: "none",
              fontSize: "2rem",
              cursor: "pointer",
            }}
          >
            &times;
          </button>
          <img
            src={selectedImage}
            alt="Enlarged cat"
            style={{
              maxWidth: "90%",
              maxHeight: "90%",
              borderRadius: "8px",
              boxShadow: "0 0 20px rgba(0, 0, 0, 0.5)",
            }}
          />
        </div>
      )}
    </div>
  );
};

export default CommentList;
