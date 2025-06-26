export interface Comment {
  id: string;
  text: string;
  location: string;
  created_at: string;
  image_url: string;
}

export interface UploadResponse {
  image_url: string;
}
