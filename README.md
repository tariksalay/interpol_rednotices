# Red Notices Data Pipeline

**Python · Selenium · RabbitMQ · PostgreSQL · Flask · Docker Compose**

A local ingestion prototype with separate collection, messaging, persistence, and presentation responsibilities. A bounded Selenium collector publishes JSON records, a consumer saves them to PostgreSQL, and a read-only Flask page displays stored rows.

## What this project demonstrates

- A producer/consumer contract with durable queue messages.
- Acknowledging messages after database commits.
- Container service boundaries, readiness dependencies, and environment configuration.

## Start here

| Read | Use it for |
| --- | --- |
| [Project walkthrough](docs/PROJECT_GUIDE.md) | Purpose, workflow, repository map, and a concrete example |
| [Code and artifact reference](docs/CODE_REFERENCE.md) | Important files, functions, classes, and their responsibilities |
| [Development guide](docs/DEVELOPMENT.md) | Setup, configuration, commands, tests, and remaining limitations |

## Explore locally

Docker and Compose are required for integration exploration.

```sh
cp .env.example .env
# Fill the two empty password settings with local URL-safe values.
docker compose config
docker compose up --build -d
# Explicit optional collection:
docker compose --profile collect run --rm container_a
```

The UI binds to `127.0.0.1:8080`. Read the development guide before collecting live data.

## Validation and scope

Six tests pass with synthetic records and mocked database/broker resources. Compose structure was checked statically; Docker builds, live service integration, Chromium behavior, and current site selectors remain unverified. This is a historical educational prototype, not an authoritative notices service.



---

[GitHub profile](https://github.com/tariksalay) · [Portfolio](https://tariksalay.github.io/) · [Earlier README](README_HISTORY.md)

The earlier README is preserved as historical context; the guides above describe this branch's implementation.
