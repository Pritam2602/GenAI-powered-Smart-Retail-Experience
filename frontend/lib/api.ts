/**
 * API service for communicating with the backend
 */

// Get API base URL from environment variable or use default
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export interface PriceRequest {
  product_name: string;
  brand: string;
  gender: string;
  category: string;
  fabric?: string;
  pattern?: string;
  color?: string;
  rating_count?: number;
  discount_percent?: number;
}

export interface PredictionResponse {
  predicted_price: number;
  product_type: string;
  model_type: string;
  confidence: string;
  timestamp: string;
  explanation?: {
    key_factors: Array<{
      factor: string;
      value: string;
      impact: string;
      description: string;
    }>;
    price_breakdown: {
      original_price: number;
      discount_amount: number;
      discount_percent: number;
      final_price: number;
    };
    recommendations: string[];
  };
}

export interface SearchRequest {
  query: string;
  k?: number;
}

export interface RecommendationItem {
  id: string;
  document: string;
  metadata: {
    brand?: string;
    price?: number;
    rating?: number;
    img?: string;
    [key: string]: any;
  };
  distance?: number;
  score?: number;
}

export interface RecommendationResponse {
  results: RecommendationItem[];
  query: string;
  total_results: number;
  timestamp: string;
}

export interface TrendingColor {
  color: string;
  popularity: number;
  trend: string;
}

export interface TrendingStyle {
  style: string;
  popularity: number;
  category: string;
}

export interface TrendResponse {
  colors?: TrendingColor[];
  styles?: TrendingStyle[];
  season?: string;
  timeframe?: string;
  category?: string;
  timestamp: string;
}

export interface HealthResponse {
  status: string;
  fast_models_loaded: boolean;
  original_model_loaded: boolean;
  recs_index_loaded: boolean;
  recs_count: number;
  embedding_model_loaded: boolean;
  model_type_in_use: string;
  timestamp: string;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: response.statusText }));
        throw new Error(error.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  // Health check
  async getHealth(): Promise<HealthResponse> {
    return this.request<HealthResponse>('/health/');
  }

  // Price prediction
  async predictPrice(
    data: PriceRequest,
    explain: boolean = false
  ): Promise<PredictionResponse> {
    const endpoint = `/predict/price${explain ? '?explain=true' : ''}`;
    return this.request<PredictionResponse>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Product recommendations
  async getRecommendations(
    query: string,
    k: number = 10
  ): Promise<RecommendationResponse> {
    return this.request<RecommendationResponse>('/recommend/products', {
      method: 'POST',
      body: JSON.stringify({ query, k }),
    });
  }

  // Trend analysis
  async getTrendingColors(timeframe: string = '30d'): Promise<TrendResponse> {
    return this.request<TrendResponse>(`/trends/colors?timeframe=${timeframe}`);
  }

  async getTrendingStyles(category: string = 'all'): Promise<TrendResponse> {
    return this.request<TrendResponse>(`/trends/styles?category=${category}`);
  }

  async getSeasonalTrends(season?: string): Promise<TrendResponse> {
    const endpoint = season ? `/trends/seasonal?season=${season}` : '/trends/seasonal';
    return this.request<TrendResponse>(endpoint);
  }

  async getPriceTrends(category: string = 'all'): Promise<any> {
    return this.request<any>(`/trends/price?category=${category}`);
  }

  async getSustainabilityTrends(): Promise<any> {
    return this.request<any>('/trends/sustainability');
  }

  async getTrendReport(): Promise<any> {
    return this.request<any>('/trends/report');
  }

  async analyzeBrands(brands: string[]): Promise<any> {
    return this.request<any>('/trends/brands', {
      method: 'POST',
      body: JSON.stringify(brands),
    });
  }
}

export const api = new ApiService();

