'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { TrendingUp, Palette, Sparkles, Leaf, DollarSign } from 'lucide-react';

export default function TrendAnalysis() {
  const [trends, setTrends] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'colors' | 'styles' | 'seasonal' | 'price' | 'sustainability'>('colors');

  useEffect(() => {
    loadTrends();
  }, [activeTab]);

  const loadTrends = async () => {
    setLoading(true);
    try {
      switch (activeTab) {
        case 'colors':
          const colors = await api.getTrendingColors('30d');
          setTrends(colors);
          break;
        case 'styles':
          const styles = await api.getTrendingStyles('all');
          setTrends(styles);
          break;
        case 'seasonal':
          const seasonal = await api.getSeasonalTrends();
          setTrends(seasonal);
          break;
        case 'price':
          const price = await api.getPriceTrends('all');
          setTrends(price);
          break;
        case 'sustainability':
          const sustainability = await api.getSustainabilityTrends();
          setTrends(sustainability);
          break;
      }
    } catch (error) {
      console.error('Failed to load trends:', error);
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'colors' as const, label: 'Colors', icon: Palette },
    { id: 'styles' as const, label: 'Styles', icon: Sparkles },
    { id: 'seasonal' as const, label: 'Seasonal', icon: TrendingUp },
    { id: 'price' as const, label: 'Price', icon: DollarSign },
    { id: 'sustainability' as const, label: 'Sustainability', icon: Leaf },
  ];

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 animate-fade-in">
      <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white">
        📊 Fashion Trend Analysis
      </h2>

      <div className="flex space-x-2 mb-6 overflow-x-auto">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors duration-200 ${
                activeTab === tab.id
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
      ) : trends && (
        <div className="space-y-4">
          {activeTab === 'colors' && trends.colors && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {trends.colors.map((color: any, idx: number) => (
                <div
                  key={idx}
                  className="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-600 rounded-lg p-4 animate-slide-up"
                  style={{ animationDelay: `${idx * 0.1}s` }}
                >
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-gray-800 dark:text-white capitalize">
                      {color.color}
                    </h4>
                    <span className={`px-2 py-1 rounded text-xs font-semibold ${
                      color.trend === 'rising' 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                        : color.trend === 'stable'
                        ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                        : 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
                    }`}>
                      {color.trend}
                    </span>
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-300">
                    Popularity: {(color.popularity * 100).toFixed(0)}%
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'styles' && trends.styles && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {trends.styles.map((style: any, idx: number) => (
                <div
                  key={idx}
                  className="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-600 rounded-lg p-4 animate-slide-up"
                  style={{ animationDelay: `${idx * 0.1}s` }}
                >
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-gray-800 dark:text-white capitalize">
                      {style.style}
                    </h4>
                    <span className="text-xs text-gray-500 dark:text-gray-400 capitalize">
                      {style.category}
                    </span>
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-300">
                    Popularity: {(style.popularity * 100).toFixed(0)}%
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'seasonal' && trends && (
            <div className="space-y-4">
              <div className="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-600 rounded-lg p-4">
                <h3 className="font-semibold text-gray-800 dark:text-white mb-4 capitalize">
                  {trends.season || 'Current Season'} Trends
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-2">Colors</h4>
                    <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-300">
                      {trends.colors?.map((color: string, idx: number) => (
                        <li key={idx} className="capitalize">• {color}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-2">Styles</h4>
                    <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-300">
                      {trends.styles?.map((style: string, idx: number) => (
                        <li key={idx} className="capitalize">• {style}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-2">Materials</h4>
                    <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-300">
                      {trends.materials?.map((material: string, idx: number) => (
                        <li key={idx} className="capitalize">• {material}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'price' && trends && (
            <div className="space-y-4">
              <div className="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-600 rounded-lg p-4">
                <h3 className="font-semibold text-gray-800 dark:text-white mb-4">
                  Price Trends
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <div className="text-sm text-gray-600 dark:text-gray-300">Average Price</div>
                    <div className="text-2xl font-bold text-gray-800 dark:text-white">
                      ₹{trends.average_price?.toLocaleString()}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600 dark:text-gray-300">Price Change</div>
                    <div className={`text-2xl font-bold ${
                      trends.price_change > 0 ? 'text-red-600' : 'text-green-600'
                    }`}>
                      {trends.price_change > 0 ? '+' : ''}{(trends.price_change * 100).toFixed(1)}%
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600 dark:text-gray-300">Trend</div>
                    <div className="text-lg font-semibold text-gray-800 dark:text-white capitalize">
                      {trends.trend_direction}
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-600 dark:text-gray-300">Seasonal Adjustment</div>
                    <div className="text-lg font-semibold text-gray-800 dark:text-white">
                      {(trends.seasonal_adjustment * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'sustainability' && trends && (
            <div className="space-y-4">
              <div className="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-600 rounded-lg p-4">
                <h3 className="font-semibold text-gray-800 dark:text-white mb-4">
                  Sustainability Trends
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Eco-Friendly Materials
                    </h4>
                    <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-300">
                      {trends.eco_friendly_materials?.map((material: string, idx: number) => (
                        <li key={idx} className="capitalize">• {material}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Consumer Interest
                    </h4>
                    <div className="text-3xl font-bold text-green-600 dark:text-green-400">
                      {(trends.consumer_interest * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

