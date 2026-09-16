FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip \
	&& python -m pip install --no-cache-dir -r requirements.txt \
	&& useradd --create-home --uid 10001 appuser

COPY api/ ./api/
COPY pipeline/ ./pipeline/
COPY static/ ./static/
COPY gunicorn_conf.py .
RUN chown -R appuser:appuser /app

USER appuser
EXPOSE 8000

ENTRYPOINT ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn_conf.py", "api.main:app"]
