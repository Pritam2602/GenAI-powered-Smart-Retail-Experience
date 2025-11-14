# 🚀 Frontend Setup Guide

## Prerequisites

- Node.js 18+ and npm/yarn
- Backend API running on http://localhost:8001 (or configure your API URL)

## Installation

### 1. Install Dependencies

```bash
cd frontend
npm install
# or
yarn install
```

### 2. Set Up Environment Variables

Create a `.env.local` file in the `frontend` directory:

```bash
cp .env.local.example .env.local
```

Edit `.env.local` and set your API URL:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
```

### 3. Start Development Server

```bash
npm run dev
# or
yarn dev
```

### 4. Open in Browser

```
http://localhost:3000
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

## 🐛 Troubleshooting

### API Connection Issues

- Check if the backend API is running
- Verify the API URL in `.env.local`
- Check CORS settings in the backend

### Build Issues

- Clear `.next` directory: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`
- Check Node.js version (requires 18+)

### TypeScript Errors

- Run `npm run build` to check for type errors
- Ensure all types are properly imported
- Check `tsconfig.json` configuration

## 📦 Production Build

```bash
npm run build
npm start
# or
yarn build
yarn start
```

## 🚀 Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Import your repository to Vercel
3. Set environment variables (NEXT_PUBLIC_API_BASE_URL)
4. Deploy!

### Netlify

1. Build the application: `npm run build`
2. Deploy the `out` directory to Netlify
3. Set environment variables in Netlify dashboard

### Docker

```bash
docker build -t smart-retail-frontend .
docker run -p 3000:3000 smart-retail-frontend
```

## 📚 Documentation

For more information, see:
- [Next.js Documentation](https://nextjs.org/docs)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [React Documentation](https://react.dev)

---

**Happy Coding! 🎉**

