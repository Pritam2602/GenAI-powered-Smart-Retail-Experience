'use client';

import { useState, useEffect } from 'react';
import { api, HealthResponse } from '@/lib/api';
import { Activity, CheckCircle, XCircle, AlertCircle } from 'lucide-react';

export default function Header() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const checkHealth = async () => {
    try {
      const healthStatus = await api.getHealth();
      setHealth(healthStatus);
      setLoading(false);
    } catch (error) {
      console.error('Health check failed:', error);
      // Set health to null if API is not available
      setHealth(null);
      setLoading(false);
    }
  };

  const getStatusIcon = () => {
    if (loading) {
      return <Activity className="w-5 h-5 text-gray-400 animate-pulse" />;
    }
    if (!health || health.status !== 'ok') {
      return <XCircle className="w-5 h-5 text-red-500" />;
    }
    return <CheckCircle className="w-5 h-5 text-green-500" />;
  };

  const getStatusText = () => {
    if (loading) return 'Checking...';
    if (!health || health.status !== 'ok') return 'API Offline';
    return 'API Online';
  };

  return (
    <header className="bg-white dark:bg-gray-800 shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4 max-w-7xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              GenAI Smart Retail
            </h1>
          </div>

          <div className="flex items-center space-x-4">
            {/* Health Status */}
            <div className="flex items-center space-x-2 px-4 py-2 bg-gray-100 dark:bg-gray-700 rounded-lg">
              {getStatusIcon()}
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                {getStatusText()}
              </span>
            </div>

            {health && health.status === 'ok' && (
              <div className="hidden md:flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
                <div className="flex items-center space-x-1">
                  {health.fast_models_loaded || health.original_model_loaded ? (
                    <CheckCircle className="w-4 h-4 text-green-500" />
                  ) : (
                    <AlertCircle className="w-4 h-4 text-yellow-500" />
                  )}
                  <span>Models</span>
                </div>
                <div className="flex items-center space-x-1">
                  {health.recs_index_loaded ? (
                    <CheckCircle className="w-4 h-4 text-green-500" />
                  ) : (
                    <AlertCircle className="w-4 h-4 text-yellow-500" />
                  )}
                  <span>Recommendations</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}

