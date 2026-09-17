# Agri-Pest Pricing Engine 🌾

An AI-powered agricultural diagnostic and mandi pricing platform built with high-throughput, production-grade systems engineering.

## 🚀 Architecture Highlights
* **Deterministic State Machine**: Agentic workflow transitions (IDLE -> ANALYZING -> RETRIEVING -> COMPLETED) with robust JSON audit logging.
* **Vector Search Retrieval**: Integrated `scikit-learn` TF-IDF embeddings to query disease treatment context via cosine similarity.
* **Advanced Caching**: Utilizes Redis to intercept redundant LLM generations and database queries, drastically reducing token consumption.
* **Resilience & Fallbacks**: Circuit breaker patterns implemented to gracefully degrade during external API timeouts or 502 Bad Gateway errors.

## ⚡ Performance & SLA Benchmarks
* **Asynchronous Concurrency**: Built with `asyncio` and semaphores to handle massive batch requests without CPU thrashing.
* **Strict Latency Gates**: Architected to strictly pass `<150ms` latency SLA gates for end-to-end processing.
* **Continuous Load Tested**: Profiled with `tracemalloc` to guarantee zero memory leaks under sustained throughput.
* **CI/CD Automation**: Fully automated GitHub Actions pipelines to enforce SLA benchmarks and state transition tests on every push.

## 🛠️ Tech Stack
* Python 3.12, FastAPI, Pytest
* Redis, scikit-learn, Numpy
* Asyncio, Memory-Profiler

## 🖥️ Production UI & Real-Time Streaming
* **Server-Sent Events (SSE)**: Implemented token-by-token streaming for generative AI responses, ensuring ultra-low perceived latency for end users.
* **WebSocket Telemetry**: Built a bi-directional WebSocket dashboard for system administrators to monitor the agent's deterministic state and token consumption in real-time.
* **Responsive Interface**: Developed a mobile-first, zero-dependency HTML/JS frontend utilizing modern Fetch API streams and CSS Flexbox.
* **Observability**: Integrated `prometheus-fastapi-instrumentator` to automatically expose OpenTelemetry metrics for production SLA monitoring.

## Deployment

The `deploy-pipeline.yml` workflow runs tests, Bandit, Safety, and a Trivy scan before publishing an immutable SHA-tagged image and `latest` to GHCR. Pull requests run verification and container scanning without publishing.

The API listens on port `8000` and exposes `GET /health` for container and load-balancer health checks. Local development can be started with `docker compose up --build`; Redis is used for distributed rate limiting and the API falls back to an in-memory limiter when Redis is unavailable.

To enable the production host rollout, create the `production` environment, set the environment variable `DEPLOY_ENABLED` to `true`, and add these environment secrets: `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`, `DEPLOY_PATH`, `GHCR_READ_USER`, and `GHCR_READ_TOKEN`. The target host needs Docker Engine and Docker Compose v2; `DEPLOY_PATH` must be writable by `DEPLOY_USER`.
