'use client';

import { useState } from 'react';
import PricePrediction from '@/components/PricePrediction';
import Recommendations from '@/components/Recommendations';
import TrendAnalysis from '@/components/TrendAnalysis';
import Header from '@/components/Header';
import { Activity, TrendingUp, Sparkles } from 'lucide-react';

export default function Home() {
  const [activeSection, setActiveSection] = useState<'prediction' | 'recommendations' | 'trends'>('prediction');

  const sections = [
    { id: 'prediction' as const, label: 'Price Prediction', icon: TrendingUp },
    { id: 'recommendations' as const, label: 'Recommendations', icon: Sparkles },
    { id: 'trends' as const, label: 'Trend Analysis', icon: Activity },
  ];

  return (
    <div className="min-h-screen">
      <Header />
      
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="text-center mb-8 animate-fade-in">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            🛍️ GenAI Smart Retail Experience
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            AI-powered fashion recommendation and price prediction system
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="flex justify-center space-x-4 mb-8 overflow-x-auto">
          {sections.map((section) => {
            const Icon = section.icon;
            return (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`flex items-center space-x-2 px-6 py-3 rounded-lg transition-all duration-200 ${
                  activeSection === section.id
                    ? 'bg-primary-600 text-white shadow-lg transform scale-105'
                    : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 shadow-md'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span className="font-semibold">{section.label}</span>
              </button>
            );
          })}
        </div>

        {/* Content Section */}
        <div className="animate-fade-in">
          {activeSection === 'prediction' && <PricePrediction />}
          {activeSection === 'recommendations' && <Recommendations />}
          {activeSection === 'trends' && <TrendAnalysis />}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8 mt-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-gray-400">
            © 2024 GenAI Smart Retail Experience. Built with Next.js, React, and TailwindCSS.
          </p>
        </div>
      </footer>
    </div>
  );
}

