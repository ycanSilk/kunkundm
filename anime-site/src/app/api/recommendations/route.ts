import { NextRequest, NextResponse } from 'next/server';
import { recommendationsStore } from '@/lib/recommendations-store';

// GET - 获取最新推荐
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const limit = parseInt(searchParams.get('limit') || '20');
    
    const recommendations = recommendationsStore.getRecommendations();
    const limitedRecommendations = recommendations.slice(0, limit);
    
    return NextResponse.json({
      success: true,
      data: limitedRecommendations,
      count: limitedRecommendations.length,
      total: recommendations.length
    });
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to fetch recommendations',
      details: error instanceof Error ? error.message : String(error)
    }, { status: 500 });
  }
}

// POST - 添加或更新推荐
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, data } = body;
    
    switch (action) {
      case 'set':
        if (!Array.isArray(data)) {
          return NextResponse.json({
            success: false,
            error: 'Data must be an array'
          }, { status: 400 });
        }
        recommendationsStore.setRecommendations(data);
        break;
        
      case 'add':
        if (!data || typeof data !== 'object') {
          return NextResponse.json({
            success: false,
            error: 'Data must be an object'
          }, { status: 400 });
        }
        recommendationsStore.addRecommendation(data);
        break;
        
      case 'clear':
        recommendationsStore.clear();
        break;
        
      default:
        return NextResponse.json({
          success: false,
          error: 'Invalid action. Use: set, add, or clear'
        }, { status: 400 });
    }
    
    return NextResponse.json({
      success: true,
      message: `Recommendations ${action} successfully`,
      count: recommendationsStore.getCount()
    });
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to update recommendations',
      details: error instanceof Error ? error.message : String(error)
    }, { status: 500 });
  }
}