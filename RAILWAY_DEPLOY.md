# Railway Deployment Guide - Hybrid Model Approach

## Quick Deploy to Railway

1. **Connect Repository**
   - Go to [Railway.app](https://railway.app)
   - Create new project from GitHub repo

2. **Add PostgreSQL Database**
   - In Railway dashboard: **+ New** → **Database** → **PostgreSQL**
   - Wait for provisioning (2-3 minutes)

3. **Set Environment Variables**
   - Click on your **Web Service** (not database)
   - Go to **Variables** tab
   - Add variables:
     - **Name**: `PGVECTOR_CONNECTION_STRING`
     - **Value**: Copy from PostgreSQL service → Connect → Postgres Connection URL
     - **Name**: `OPENROUTER_API_KEY`
     - **Value**: Your OpenRouter API key from https://openrouter.ai/keys

4. **Deploy**
   - Railway auto-deploys using the Dockerfile
   - Build time: 8-12 minutes (embedding model download once)
   - Subsequent deployments are faster (3-5 minutes)

## Hybrid Model Benefits

✅ **Cost Optimization**
- Local embeddings = No API costs for vector operations
- OpenRouter API = Pay only for language generation
- ~90% cost reduction vs full API approach

✅ **Model Flexibility**
- Access to multiple models: Claude, GPT, Llama, Gemma
- Switch models without code changes
- Free tier models available (Llama, Gemma)

✅ **Performance Balance**
- Fast local embeddings (no API latency)
- High-quality responses from premium models
- Moderate memory usage (~500MB)

✅ **Deployment Stability**
- Only sentence-transformers download needed
- Much smaller than full LLM (300MB vs 1GB+)
- Reliable builds with reduced timeout risk

## Available Models

### Free Models (Default: gpt-oss-120b)
- `openai/gpt-oss-120b:free` ⭐ **DEFAULT** - Large 120B parameter model
- `meta-llama/llama-3.1-8b-instruct:free`
- `google/gemma-2-9b-it:free`

### Premium Models
- `anthropic/claude-3-haiku` (~$0.25/1M tokens)
- `openai/gpt-3.5-turbo` (~$0.50/1M tokens)
- `microsoft/wizardlm-2-8x22b` (~$1.00/1M tokens)

## Environment Variables Required

```bash
PGVECTOR_CONNECTION_STRING=postgresql://username:password@host:port/database
OPENROUTER_API_KEY=sk-or-your-openrouter-api-key-here
```

## Expected Costs

- **Embeddings**: FREE (local model)
- **Language Model**: $0.001-0.01 per question (varies by model)
- **Railway**: Free tier covers most usage
- **PostgreSQL**: Included in Railway

## Architecture Benefits

- **Embeddings**: Local HuggingFace model (fast, free, offline)
- **Language Model**: OpenRouter API (flexible, high-quality)
- **Vector Store**: PostgreSQL with PGVector
- **Memory Usage**: ~500MB (balanced approach)
- **Build Time**: 8-12 minutes first time, 3-5 minutes subsequent

## Model Selection

The app includes a model selector in the sidebar:
- Choose based on your needs (speed vs quality vs cost)
- Free models for development/testing
- Premium models for production

## Troubleshooting

- **API Key Error**: Ensure OPENROUTER_API_KEY is set correctly
- **Model Access**: Some models may require OpenRouter credits
- **Embedding Load**: First run downloads ~300MB model
- **Database**: Check PGVECTOR_CONNECTION_STRING format