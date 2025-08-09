# Docker Setup for LLM Geolocation

## Quick Start

1. **Set your API keys:**
   ```bash
   export OPENAI_API_KEY="your-openai-key"
   export GOOGLE_MAPS_API_KEY="your-google-key"
   ```

2. **Build and run:**
   ```bash
   docker-compose up --build
   ```

## Manual Docker Commands

**Build the image:**
```bash
docker build -t llm-geolocation .
```

**Run experiments:**
```bash
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -v $(pwd)/runs:/app/runs llm-geolocation python3 run_experiment.py --method M-2 --eval-set validation-dev-A.csv
```

**Interactive shell:**
```bash
docker run -it -e OPENAI_API_KEY=$OPENAI_API_KEY llm-geolocation /bin/bash
```

## Reproducibility

This Docker container locks in:
- Python 3.11
- Exact package versions from requirements.txt  
- OpenAI API endpoints as of April 2025
- All project dependencies

Results should be identical across different machines. 