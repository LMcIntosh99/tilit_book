import { useForm } from "react-hook-form";
import axios from "axios";
import { type NewComment } from "../types/index";

interface Props {
  onNewComment: () => void;
}

const CommentForm = ({ onNewComment }: Props) => {
  const { register, handleSubmit, reset } = useForm<NewComment>();

  const onSubmit = async (data: NewComment) => {
    await axios.post("/api/comments", data);
    onNewComment();
    reset();
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <textarea {...register("text")} placeholder="Where did you find him?" required />
      <input {...register("location")} placeholder="Your location" required />
      <button type="submit">Submit</button>
    </form>
  );
};

export default CommentForm;