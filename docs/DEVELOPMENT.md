# Development and validation

This modernization guide supersedes the historical README's three-container startup details. The new Compose stack separates PostgreSQL, RabbitMQ, the consumer, and the read-only web UI. The Selenium collector is explicitly opt-in.

```sh
cp .env.example .env
# Fill both empty password values with locally generated URL-safe letters/digits.
docker compose config
docker compose up --build -d
# Optional, after checking the upstream site's current access rules:
docker compose --profile collect run --rm container_a
```

The UI binds only to `127.0.0.1:8080`. Broker/database ports are internal. `MAX_PAGES` defaults to 1. Chromium's sandbox remains enabled; `CHROME_NO_SANDBOX=1` is an explicit compatibility option if the container runtime cannot support it. No live scraping is performed by tests. Upstream markup may have changed, and the Selenium pagination selectors need live verification before collecting multiple pages.

The producer sends durable JSON messages with publisher confirmations. The consumer validates fields, inserts with parameters, and acknowledges only after commit. Invalid messages are rejected without requeueing; database errors requeue and stop the worker for its restart policy. Delivery is at least once: a crash after commit but before ack can duplicate records. Stable upstream identifiers/idempotency remain future work. Re-running collection appends records rather than replacing the database.

Named volumes retain data. The schema is initialized by PostgreSQL on a fresh volume. Old database volumes require an explicit migration; no data is deleted or migrated automatically. The old PostgreSQL startup/config files are historical and are no longer used by the Dockerfile.

For unit tests, use Python 3.12 and install `Container_A/reqs.txt` and `Container_B/reqs.txt`, then run `python -m unittest discover -s tests -v`. Tests use synthetic notices and database/broker mocks. Docker image builds, live PostgreSQL/RabbitMQ integration, browser sandbox compatibility, and the live site have not been tested here. Treat this as a local proof of concept, not a production notices service.
