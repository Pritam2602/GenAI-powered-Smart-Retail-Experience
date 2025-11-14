# 🛍️ GenAI Smart Retail Experience - Frontend

Modern, responsive frontend for the GenAI-powered Smart Retail Experience built with Next.js, React, and TailwindCSS.

## ✨ Features

- **💰 Price Prediction**: AI-powered price prediction with explainability
- **🔍 Product Recommendations**: Semantic search for fashion products
- **📊 Trend Analysis**: Fashion trend analysis and insights
- **🎨 Modern UI**: Beautiful, responsive design with TailwindCSS
- **🌙 Dark Mode**: Support for dark mode (automatic based on system preference)
- **⚡ Fast**: Built with Next.js for optimal performance
- **📱 Responsive**: Works on all devices (mobile, tablet, desktop)

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn
- Backend API running on http://localhost:8001

### Installation

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   # or
   yarn install
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local and set NEXT_PUBLIC_API_BASE_URL to your API URL
   ```

3. **Run development server**:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Open in browser**:
   ```
   http://localhost:3000
   ```

## 📁 Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page
│   └── globals.css         # Global styles
├── components/
│   ├── Header.tsx          # Header component
│   ├── PricePrediction.tsx # Price prediction component
│   ├── Recommendations.tsx # Recommendations component
│   └── TrendAnalysis.tsx   # Trend analysis component
├── lib/
│   └── api.ts              # API service
├── public/                 # Static files
├── package.json            # Dependencies
├── tailwind.config.js      # TailwindCSS configuration
├── tsconfig.json           # TypeScript configuration
└── next.config.js          # Next.js configuration
```

## 🎨 Features

### Price Prediction
- Input form for product details
- Real-time price prediction
- Optional explanation with key factors
- Price breakdown and recommendations

### Product Recommendations
- Semantic search for products
- Configurable number of results
- Product cards with metadata
- Similarity scores

### Trend Analysis
- Trending colors
- Trending styles
- Seasonal trends
- Price trends
- Sustainability trends

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file in the `frontend` directory:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
```

### API Configuration

The frontend connects to the backend API. Make sure the backend is running on the configured URL.

## 📦 Build for Production

1. **Build the application**:
   ```bash
   npm run build
   # or
   yarn build
   ```

2. **Start production server**:
   ```bash
   npm start
   # or
   yarn start
   ```

## 🚀 Deployment

### Deploy to Vercel

1. Push your code to GitHub
2. Import your repository to Vercel
3. Set environment variables
4. Deploy!

### Deploy to Netlify

1. Build the application: `npm run build`
2. Deploy the `out` directory to Netlify
3. Set environment variables in Netlify dashboard

## 🎨 Styling

This project uses TailwindCSS for styling. Customize the theme in `tailwind.config.js`.

## 📱 Responsive Design

The frontend is fully responsive and works on:
- Mobile devices (320px+)
- Tablets (768px+)
- Desktop (1024px+)
- Large screens (1280px+)

## 🐛 Troubleshooting

### API Connection Issues

- Check if the backend API is running
- Verify the API URL in `.env.local`
- Check CORS settings in the backend

### Build Issues

- Clear `.next` directory: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`
- Check Node.js version (requires 18+)

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Next.js for the excellent React framework
- TailwindCSS for the utility-first CSS framework
- React for the UI library
- Framer Motion for animations

