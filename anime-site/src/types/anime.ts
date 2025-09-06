export interface Anime {
  id: string;
  title: string;
  episode: string;
  imageUrl?: string;
  description?: string;
  genres: string[];
  rating: number;
  releaseDate: string;
  url: string;
}

export interface WeeklyUpdate {
  day: string;
  anime: Anime[];
  count: number;
}

export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}