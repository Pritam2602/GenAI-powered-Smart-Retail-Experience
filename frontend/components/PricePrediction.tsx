'use client';

import { useState } from 'react';
import { api, PriceRequest, PredictionResponse } from '@/lib/api';
import { TrendingUp, TrendingDown, Info, Loader2 } from 'lucide-react';

export default function PricePrediction() {
  const [formData, setFormData] = useState<PriceRequest>({
    product_name: '',
    brand: '',
    gender: 'men',
    category: '',
    fabric: '',
    pattern: '',
    color: '',
    rating_count: 0,
    discount_percent: 0,
  });
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [explain, setExplain] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const prediction = await api.predictPrice(formData, explain);
      setResult(prediction);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to predict price');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'rating_count' || name === 'discount_percent' 
        ? parseFloat(value) || 0 
        : value,
    }));
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 animate-fade-in">
      <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white">
        💰 Price Prediction
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Product Name *
            </label>
            <input
              type="text"
              name="product_name"
              value={formData.product_name}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              placeholder="e.g., Men Solid Casual Shirt"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Brand *
            </label>
            <input
              type="text"
              name="brand"
              value={formData.brand}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              placeholder="e.g., roadster"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Gender *
            </label>
            <select
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            >
              <option value="men">Men</option>
              <option value="women">Women</option>
              <option value="unisex">Unisex</option>
              <option value="boys">Boys</option>
              <option value="girls">Girls</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Category *
            </label>
            <input
              type="text"
              name="category"
              value={formData.category}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              placeholder="e.g., shirt, jeans, dress"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Fabric
            </label>
            <input
              type="text"
              name="fabric"
              value={formData.fabric}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              placeholder="e.g., cotton, polyester"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Pattern
            </label>
            <input
              type="text"
              name="pattern"
              value={formData.pattern}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              placeholder="e.g., solid, striped"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Color
            </label>
            <input
              type="text"
              name="color"
              value={formData.color}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              placeholder="e.g., blue, red"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Rating Count
            </label>
            <input
              type="number"
              name="rating_count"
              value={formData.rating_count}
              onChange={handleChange}
              min="0"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Discount Percentage
            </label>
            <input
              type="number"
              name="discount_percent"
              value={formData.discount_percent}
              onChange={handleChange}
              min="0"
              max="100"
              step="0.1"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            />
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <input
            type="checkbox"
            id="explain"
            checked={explain}
            onChange={(e) => setExplain(e.target.checked)}
            className="w-4 h-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
          />
          <label htmlFor="explain" className="text-sm text-gray-700 dark:text-gray-300">
            Include explanation (shows key factors and feature contributions)
          </label>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin" />
              <span>Predicting...</span>
            </>
          ) : (
            <span>Predict Price</span>
          )}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-6 p-6 bg-gradient-to-br from-primary-50 to-primary-100 dark:from-gray-700 dark:to-gray-600 rounded-lg animate-slide-up">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-gray-800 dark:text-white">
              Predicted Price
            </h3>
            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
              result.confidence === 'High' 
                ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                : result.confidence === 'Medium'
                ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                : 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200'
            }`}>
              {result.confidence} Confidence
            </span>
          </div>

          <div className="text-4xl font-bold text-primary-600 dark:text-primary-400 mb-2">
            ₹{result.predicted_price.toFixed(2)}
          </div>

          <div className="grid grid-cols-2 gap-4 mt-4 text-sm">
            <div>
              <span className="text-gray-600 dark:text-gray-300">Product Type:</span>
              <span className="ml-2 font-semibold text-gray-800 dark:text-white capitalize">
                {result.product_type.replace('_', ' ')}
              </span>
            </div>
            <div>
              <span className="text-gray-600 dark:text-gray-300">Model Type:</span>
              <span className="ml-2 font-semibold text-gray-800 dark:text-white capitalize">
                {result.model_type.replace('_', ' ')}
              </span>
            </div>
          </div>

          {result.explanation && (
            <div className="mt-6 space-y-4">
              <h4 className="font-semibold text-gray-800 dark:text-white flex items-center space-x-2">
                <Info className="w-5 h-5" />
                <span>Explanation</span>
              </h4>

              <div className="bg-white dark:bg-gray-800 rounded-lg p-4">
                <h5 className="font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Key Factors:
                </h5>
                <ul className="space-y-2">
                  {result.explanation.key_factors.map((factor, idx) => (
                    <li key={idx} className="flex items-start space-x-2">
                      {factor.impact === 'high' ? (
                        <TrendingUp className="w-4 h-4 text-red-500 mt-1" />
                      ) : factor.impact === 'medium' ? (
                        <TrendingDown className="w-4 h-4 text-yellow-500 mt-1" />
                      ) : (
                        <Info className="w-4 h-4 text-gray-500 mt-1" />
                      )}
                      <span className="text-sm text-gray-600 dark:text-gray-300">
                        <span className="font-semibold">{factor.factor}:</span> {factor.description}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>

              {result.explanation.price_breakdown && (
                <div className="bg-white dark:bg-gray-800 rounded-lg p-4">
                  <h5 className="font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Price Breakdown:
                  </h5>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div>
                      <span className="text-gray-600 dark:text-gray-300">Original Price:</span>
                      <span className="ml-2 font-semibold text-gray-800 dark:text-white">
                        ₹{result.explanation.price_breakdown.original_price.toFixed(2)}
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-600 dark:text-gray-300">Discount:</span>
                      <span className="ml-2 font-semibold text-red-600 dark:text-red-400">
                        -₹{result.explanation.price_breakdown.discount_amount.toFixed(2)}
                      </span>
                    </div>
                  </div>
                </div>
              )}

              {result.explanation.recommendations && result.explanation.recommendations.length > 0 && (
                <div className="bg-white dark:bg-gray-800 rounded-lg p-4">
                  <h5 className="font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Recommendations:
                  </h5>
                  <ul className="list-disc list-inside space-y-1 text-sm text-gray-600 dark:text-gray-300">
                    {result.explanation.recommendations.map((rec, idx) => (
                      <li key={idx}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

