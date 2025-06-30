import { useEffect, useState } from "react";
import axios from "axios";
import { type Comment } from "../types";

const CommentList = () => {
  const [comments, setComments] = useState<Comment[]>([]);

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
          className="w-full max-w-xs rounded-lg mt-2"
        />
      )}
  </div>
)) : <p>Loading comments...</p>}
    </div>
  );
};

export default CommentList;