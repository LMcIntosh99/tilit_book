import { useForm } from "react-hook-form";
import axios from "axios";

interface Props {
  onUpload: (url: string) => void;
}

const UploadForm = ({ onUpload }: Props) => {
  const { register, handleSubmit, reset } = useForm();

  const onSubmit = async (data: any) => {
    const formData = new FormData();
    formData.append("file", data.file[0]);
    const res = await axios.post("/api/upload", formData);
    onUpload(res.data.imageUrl);
    reset();
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input type="file" {...register("file")} required />
      <button type="submit">Upload</button>
    </form>
  );
};

export default UploadForm;
