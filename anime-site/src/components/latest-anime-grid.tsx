import Image from 'next/image';
import Link from 'next/link';
import fs from 'fs';
import path from 'path';

interface AnimeCard {
  id: string;
  title: string;
  coverImage: string;
  episodes: number;
  currentEpisode: number;
  genre: string[];
}

interface CrawlerData {
  success: boolean;
  total_count: number;
  data: Array<{
    cover_image: string;
    title: string;
    detail_url: string;
    current_episode: number;
  }>;
}

async function getLatestAnimeData(): Promise<AnimeCard[]> {
  try {
    const dataPath = path.join(process.cwd(), 'data', 'latest_updates.json');
    const fileContents = fs.readFileSync(dataPath, 'utf8');
    const data: CrawlerData = JSON.parse(fileContents);
    
    if (!data.success || !data.data) {
      throw new Error('Invalid data format');
    }

    return data.data.map((item, index) => ({
      id: item.detail_url.split('/').pop()?.replace('.html', '') || String(index + 1),
          detailUrl: item.detail_url,
      title: item.title,
      coverImage: item.cover_image,
      episodes: item.current_episode,
      currentEpisode: item.current_episode,
      genre: ['最新', '热门']
    }));
  } catch (error) {
    console.error('Failed to load latest anime data:', error);
    return [];
  }
}

export async function LatestAnimeGrid() {
  const animeList = await getLatestAnimeData();
  return (
    <div className=" w-full">
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-4 xl:grid-cols-4 gap-2 sm:gap-3 md:gap-4">
        {animeList.slice(0, 8).map((anime) => (
          <div
            key={anime.id}
            className="group cursor-pointer rounded-lg border border-gray-200 bg-white p-2 transition-all duration-300 hover:scale-105 hover:border-purple-300 hover:shadow-md"
          >
            <Link href={`/anime/${anime.id}`}>
              <div className="space-y-2">
                {/* 封面 */}
                <div className="aspect-[3/4] overflow-hidden rounded-md">
                  <Image
                    src={anime.coverImage}
                    alt={anime.title}
                    width={300}
                    height={400}
                    className="h-full w-full object-cover"
                  />
                </div>
                
                {/* 名称 */}
                <h3 className="text-xs sm:text-sm font-medium text-gray-900 line-clamp-2 text-center">
                  {anime.title}
                </h3>
                
                {/* 集数 */}
                <p className="text-xs text-gray-600 text-center">
                  最新：第{anime.currentEpisode}集
                </p>
              </div>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}