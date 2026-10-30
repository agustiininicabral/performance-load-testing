# Performance & Load Testing

A reproducible performance-testing project using Locust and a small FastAPI service. It provides a local target application, concurrent user scenarios, response-time statistics, CSV/HTML reports and a CI load-smoke test.

## What it measures

- Request count and throughput (requests per second).
- Average, median, p90, p95 and p99 response times.
- Failure count and failure ratio.
- Mixed traffic across health checks, product browsing and a CPU-bound compute endpoint.
- Reproducible load profiles with configurable users, spawn rate and duration.

## Install and run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
```

Terminal 1 — start the local target:

```bash
uvicorn load_testing.app:app --host 127.0.0.1 --port 8000
```

Terminal 2 — execute a load test:

```bash
locust -f locust/locustfile.py --host http://127.0.0.1:8000
```

Open the Locust UI at `http://localhost:8089`, or run headlessly:

```bash
locust -f locust/locustfile.py --headless --host http://127.0.0.1:8000 \
  -u 20 -r 4 -t 60s --exit-code-on-error 1 \
  --csv output/load-test --html output/load-test-report.html
```

## API under test

- `GET /health`: lightweight availability endpoint.
- `GET /products?limit=20`: product listing with bounded page size.
- `POST /compute`: deterministic CPU work controlled by an iteration count.

The target service is intentionally local and deterministic. It is not intended to represent the performance of a production system.

## CI

GitHub Actions runs unit/API tests on Python 3.11, 3.12 and 3.13. A separate smoke-load job starts the local API, waits for readiness, runs a short headless Locust test and uploads the generated CSV/HTML reports.

## Interpreting results

Do not compare runs across different runner sizes or network environments as if they were equivalent. Use a stable target environment, repeat tests, record the workload profile and compare p95/p99 latency and failure rate. The CI load test is a functional smoke test, not a production capacity benchmark.

## License

MIT. See [LICENSE](LICENSE).
