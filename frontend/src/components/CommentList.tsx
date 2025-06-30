import { useEffect, useState } from "react";
import axios from "axios";
import { type Comment } from "../types";

const CommentList = () => {
  const [comments, setComments] = useState<Comment[]>([]);
  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  useEffect(() => {
    axios.get("http://localhost:8000/comments")
      .then(res => {
        setComments(res.data);
      })
      .catch(err => {
        console.error("Failed to load comments", err);
      });
  }, []);

  return (
    <div>
      <h3>Comments</h3>
      {Array.isArray(comments) ? comments.map((c) => (
        <div key={c.id}>
          <p>{c.text}</p>
          <small>{c.location} – {new Date(c.created_at).toLocaleString()}</small>
          {c.image_url && (
            <img
              src={c.image_url}
              alt="Cat"
              style={{ cursor: 'pointer', maxWidth: '200px' }}
              onClick={() => setSelectedImage(c.image_url)}
            />
          )}
        </div>
      )) : <p>Loading comments...</p>}

      {/* Modal/Overlay for enlarged image */}
      {selectedImage && (
        <div
          onClick={() => setSelectedImage(null)}
          style={{
            position: 'fixed',
            top: 0, left: 0,
            width: '100vw', height: '100vh',
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
          }}
        >
          <img
            src={selectedImage}
            alt="Enlarged cat"
            style={{
              maxWidth: '90%',
              maxHeight: '90%',
              borderRadius: '8px',
              boxShadow: '0 0 20px rgba(0, 0, 0, 0.5)',
            }}
          />
        </div>
      )}
    </div>
  );
};

export default CommentList;
