import { useState } from "react";
import UploadForm from "../components/UploadForm";
import CommentForm from "../components/CommentForm";
import CommentList from "../components/CommentList";

const Home = () => {
  const [imageUrl, setImageUrl] = useState<string>("");

  return (
    <div>
      <h1>Have you seen Tilit?</h1>
      <img src={imageUrl || "/tilit_home.jpeg"} alt="Cat" width="300" />
      <UploadForm onUpload={setImageUrl} />
      <CommentForm onNewComment={() => window.location.reload()} />
      <CommentList />
    </div>
  );
};

export default Home;
