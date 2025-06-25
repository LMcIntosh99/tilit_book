export interface Comment {
  id: string;
  text: string;
  location: string;
  createdAt: string;
}

export interface UploadResponse {
  imageUrl: string;
}

export interface NewComment {
  text: string;
  location: string;
}
