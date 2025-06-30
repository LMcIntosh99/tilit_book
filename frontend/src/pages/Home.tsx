import { useEffect, useState } from "react";
import CommentForm from "../components/CommentForm";
import CommentList from "../components/CommentList";

const Home = () => {
  const [imageUrl, setImageUrl] = useState<string>("/tilit_home.jpeg");
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleNewComment = () => {
    // Trigger a refresh without reloading the page
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <div className="min-h-screen bg-[#121212] text-white px-4 py-8">
      <div className="text-center mb-10">
        <h1 className="text-4xl md:text-5xl font-bold text-orange-500 mb-4">
          Have you seen Tilit?
        </h1>
        <img
          src={imageUrl}
          alt="Tilit the cat"
          className="rounded-lg shadow-lg max-h-[400px] mx-auto"
          width="300" 
        />
      </div>
      <CommentForm onNewComment={handleNewComment} />
      <CommentList key={refreshTrigger} />
    </div>
  );
};

export default Home;
