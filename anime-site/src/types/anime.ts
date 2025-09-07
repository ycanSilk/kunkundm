export interface Anime {
  id: string;
  title: string;
  episodes?: number;
  episode?: string;
  imageUrl?: string;
  coverImage?: string;
  description?: string;
  genres?: string[];
  rating?: number;
  releaseDate?: string;
  year?: number;
  type?: string;
  url?: string;
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