'use client';

import { useState } from 'react';
import { api, RecommendationResponse } from '@/lib/api';
import { Search, Loader2, Star, ShoppingBag } from 'lucide-react';

export default function Recommendations() {
  const [query, setQuery] = useState('');
  const [k, setK] = useState(10);
  const [results, setResults] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const recommendations = await api.getRecommendations(query, k);
      setResults(recommendations);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get recommendations');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 animate-fade-in">
      <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white">
        🔍 Product Recommendations
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Search Query *
          </label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              required
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              placeholder="e.g., blue denim jacket for men"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Number of Results: {k}
          </label>
          <input
            type="range"
            min="1"
            max="50"
            value={k}
            onChange={(e) => setK(parseInt(e.target.value))}
            className="w-full"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin" />
              <span>Searching...</span>
            </>
          ) : (
            <>
              <Search className="w-5 h-5" />
              <span>Get Recommendations</span>
            </>
          )}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {results && (
        <div className="mt-6 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-800 dark:text-white">
              Results ({results.total_results})
            </h3>
            <span className="text-sm text-gray-600 dark:text-gray-300">
              Query: "{results.query}"
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {results.results.map((item, idx) => (
              <div
                key={idx}
                className="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-600 rounded-lg p-4 hover:shadow-lg transition-shadow duration-200 animate-slide-up"
                style={{ animationDelay: `${idx * 0.1}s` }}
              >
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-semibold text-gray-800 dark:text-white text-sm line-clamp-2">
                    {item.document}
                  </h4>
                  {item.score && (
                    <span className="text-xs bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-200 px-2 py-1 rounded">
                      {(item.score * 100).toFixed(0)}%
                    </span>
                  )}
                </div>

                <div className="space-y-2 mt-3">
                  {item.metadata.brand && (
                    <div className="flex items-center space-x-1 text-xs text-gray-600 dark:text-gray-300">
                      <ShoppingBag className="w-3 h-3" />
                      <span className="font-medium">{item.metadata.brand}</span>
                    </div>
                  )}

                  {item.metadata.price && (
                    <div className="text-lg font-bold text-primary-600 dark:text-primary-400">
                      ₹{item.metadata.price.toLocaleString()}
                    </div>
                  )}

                  {item.metadata.rating && (
                    <div className="flex items-center space-x-1 text-xs">
                      <Star className="w-3 h-3 text-yellow-500 fill-yellow-500" />
                      <span className="text-gray-600 dark:text-gray-300">
                        {item.metadata.rating}
                      </span>
                    </div>
                  )}

                  {item.distance !== undefined && (
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      Distance: {item.distance.toFixed(3)}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

