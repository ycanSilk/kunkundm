// 最新推荐数据存储
interface Recommendation {
  id: string;
  title: string;
  coverImage: string;
  description: string;
  rating: number;
  genres: string[];
  year: number;
  episodes: number;
  updatedAt: string;
}

class RecommendationsStore {
  private recommendations: Recommendation[] = [];

  // 设置最新推荐
  setRecommendations(data: Recommendation[]) {
    this.recommendations = data;
  }

  // 获取最新推荐
  getRecommendations(): Recommendation[] {
    return this.recommendations;
  }

  // 添加单条推荐
  addRecommendation(item: Recommendation) {
    this.recommendations.unshift(item);
    // 保持最多50条推荐
    if (this.recommendations.length > 50) {
      this.recommendations = this.recommendations.slice(0, 50);
    }
  }

  // 获取推荐数量
  getCount(): number {
    return this.recommendations.length;
  }

  // 清空推荐
  clear() {
    this.recommendations = [];
  }
}

export const recommendationsStore = new RecommendationsStore();