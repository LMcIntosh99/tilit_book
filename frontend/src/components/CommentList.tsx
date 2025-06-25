import { useEffect, useState } from "react";
import axios from "axios";
import { type Comment } from "../types";

const CommentList = () => {
  const [comments, setComments] = useState<Comment[]>([]);

  useEffect(() => {
  axios.get("/api/comments")
    .then(res => {
      console.log("API response:", res.data);
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
    <small>{c.location} – {new Date(c.createdAt).toLocaleString()}</small>
  </div>
)) : <p>Loading comments...</p>}
    </div>
  );
};

export default CommentList;