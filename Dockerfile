# Production Dockerfile for Agri-Pest Backend + Frontend UI
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies first (caches this layer to speed up future builds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the core architecture and UI static files
COPY api/ ./api/
COPY static/ ./static/
COPY gunicorn_conf.py .

# Expose the production port
EXPOSE 8000

# Start the high-performance Gunicorn server utilizing your dynamic Uvicorn workers
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn_conf.py", "api.main:app"]
