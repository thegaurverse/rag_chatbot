# Railway Deployment Guide

## Quick Deploy to Railway

1. **Connect Repository**
   - Go to [Railway.app](https://railway.app)
   - Create new project from GitHub repo

2. **Add PostgreSQL Database**
   - In Railway dashboard: **+ New** → **Database** → **PostgreSQL**
   - Wait for provisioning (2-3 minutes)

3. **Set Environment Variable**
   - Click on your **Web Service** (not database)
   - Go to **Variables** tab
   - Add variable:
     - **Name**: `PGVECTOR_CONNECTION_STRING`
     - **Value**: Copy from PostgreSQL service → Connect → Postgres Connection URL

4. **Deploy**
   - Railway auto-deploys from your repo
   - First deployment takes 5-10 minutes (model downloads)
   - Subsequent deployments are faster

## Optimizations Applied

✅ **Build Timeout Prevention**
- Removed `release` command from Procfile
- Moved database initialization to runtime
- Added lazy model loading with caching

✅ **Performance Improvements**
- Models download at runtime (not build time)
- Streamlit caching for models and embeddings
- Session state management to prevent reloading

✅ **Error Handling**
- Graceful model loading failures
- Database connection retries
- User-friendly error messages

## Expected Behavior

1. **First Run**: May take 2-3 minutes to load models
2. **Subsequent Runs**: Fast response (~2-5 seconds)
3. **Memory Usage**: ~1.8GB (well within Railway's 8GB limit)

## Troubleshooting

- **Build timeout**: Models now load at runtime, not build time
- **Memory issues**: App uses ~1.8GB RAM, suitable for Railway
- **Database errors**: Check connection string format
- **Slow first response**: Normal - models are downloading

## Test Questions
- "What is HALE?"
- "What are the main health indicators?"
- "How is life expectancy calculated?"