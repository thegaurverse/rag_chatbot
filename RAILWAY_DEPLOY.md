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
   - Railway auto-deploys using the Dockerfile
   - First deployment takes 8-15 minutes (model downloads)
   - Subsequent deployments are faster (5-8 minutes)

## RPC Error Solutions Applied

✅ **Custom Dockerfile Approach**
- Uses Python 3.11-slim base image
- Installs system dependencies (gcc, g++)
- Optimized pip install with timeouts and retries
- Better layer caching for faster rebuilds

✅ **Railway Configuration**
- `railway.json` specifies Dockerfile builder
- Restart policy for failed deployments
- Proper port configuration

✅ **Optimized Dependencies**
- Compatible version ranges for all packages
- Reduced numpy version conflicts
- Streamlined requirements.txt

✅ **Build Optimizations**
- `.dockerignore` excludes unnecessary files
- Better caching strategy
- Headless Streamlit configuration

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