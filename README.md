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
