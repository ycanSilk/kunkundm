// 初始化推荐数据脚本
import { recommendationsStore } from '@/lib/recommendations-store';
import { getMockRecommendations } from '@/lib/mock-recommendations';

// 初始化推荐数据
export function initRecommendations() {
  const mockData = getMockRecommendations(5);
  recommendationsStore.setRecommendations(mockData);
  console.log('✅ Recommendations initialized with', mockData.length, 'items');
  return mockData;
}

// 如果是直接运行
if (require.main === module) {
  initRecommendations();
}