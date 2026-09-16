import multiprocessing

# Industry standard: 2 workers per CPU core + 1
cores = multiprocessing.cpu_count()
workers_per_core = 2
workers = max(int(float(cores) * workers_per_core) + 1, 2)

bind = "0.0.0.0:8000"
# Tell Gunicorn to use Uvicorn's high-performance async workers
worker_class = "uvicorn.workers.UvicornWorker"
loglevel = "info"
accesslog = "-"
errorlog = "-"

print(f"🚀 Starting Gunicorn with {workers} Uvicorn workers on {cores} CPU cores...")
