# Deployment Guide for GenAI Fashion Hub

This guide will help you deploy your GenAI Fashion Hub application to production using Render for the backend and Streamlit Community Cloud for the frontend.

## Prerequisites

1. GitHub repository with your code
2. Render account (free tier available)
3. Streamlit Community Cloud account (free)

## Step 1: Deploy FastAPI Backend to Render

### 1.1 Prepare Your Repository

Make sure your repository contains:
- `server/app.py` (FastAPI application)
- `requirements.txt` (Python dependencies)
- `render.yaml` (Render configuration)
- `Procfile` (Process configuration)
- `artifacts/` folder with your trained models
- `chroma_db/` folder with your vector database

### 1.2 Deploy to Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `smart-retail-api` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server.app:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

5. Click "Create Web Service"

### 1.3 Upload Model Files

Since Render's free tier has file size limits, you'll need to upload your model files:

1. **Option A: Use Git LFS (Recommended)**
   ```bash
   git lfs install
   git lfs track "*.joblib"
   git lfs track "chroma_db/**"
   git add .gitattributes
   git commit -m "Add LFS tracking"
   git push
   ```

2. **Option B: Upload to Cloud Storage**
   - Upload `artifacts/` and `chroma_db/` to Google Drive, Dropbox, or AWS S3
   - Modify `server/app.py` to download files on startup

### 1.4 Get Your API URL

After deployment, Render will give you a URL like:
`https://smart-retail-api.onrender.com`

## Step 2: Deploy Streamlit Frontend

### 2.1 Update API URL

In your `streamlit_app.py`, the app will automatically use the production API URL when deployed to Streamlit Community Cloud.

### 2.2 Deploy to Streamlit Community Cloud

1. Go to [Streamlit Community Cloud](https://share.streamlit.io/)
2. Click "New app"
3. Connect your GitHub repository
4. Configure:
   - **Repository**: Your GitHub repo
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **App URL**: Choose your preferred URL

5. Add environment variable:
   - **Key**: `API_BASE_URL`
   - **Value**: `https://your-render-app-name.onrender.com`

6. Click "Deploy"

## Step 3: Test Your Deployment

1. **Test Backend**: Visit your Render URL + `/healthz`
   - Example: `https://smart-retail-api.onrender.com/healthz`
   - Should return JSON with status information

2. **Test Frontend**: Visit your Streamlit app URL
   - Should load the interface
   - API Health Check should show "Connected"
   - Try price prediction and recommendations

## Troubleshooting

### Common Issues

1. **"Connection failed" error**
   - Check that your Render backend is running
   - Verify the API_BASE_URL environment variable in Streamlit
   - Test the backend URL directly in browser

2. **Model files not found**
   - Ensure model files are uploaded to Render
   - Check file paths in your code
   - Consider using cloud storage for large files

3. **ChromaDB issues**
   - Make sure `chroma_db/` folder is uploaded
   - Check file permissions
   - Verify the database path in your code

4. **Slow startup**
   - Render free tier has cold starts
   - Consider upgrading to paid plan for better performance
   - Optimize model loading

### Performance Tips

1. **For Production**:
   - Upgrade to Render's paid plan for better performance
   - Use Redis for caching
   - Implement connection pooling
   - Add health checks and monitoring

2. **For Development**:
   - Use local development with `http://127.0.0.1:8001`
   - Test with smaller datasets
   - Use environment variables for configuration

## Environment Variables

### Backend (Render)
- `PYTHON_VERSION`: `3.10.0`
- `PORT`: Automatically set by Render

### Frontend (Streamlit)
- `API_BASE_URL`: Your Render backend URL

## File Structure for Deployment

```
your-repo/
├── server/
│   └── app.py
├── artifacts/
│   ├── fast_price_models_api.joblib
│   └── price_model.joblib
├── chroma_db/
│   └── (ChromaDB files)
├── streamlit_app.py
├── requirements.txt
├── render.yaml
├── Procfile
└── DEPLOYMENT_GUIDE.md
```

## Support

If you encounter issues:
1. Check Render logs in the dashboard
2. Check Streamlit logs in the Community Cloud
3. Test API endpoints directly
4. Verify environment variables
5. Check file uploads and permissions
