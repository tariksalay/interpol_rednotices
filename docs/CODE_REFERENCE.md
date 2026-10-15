# Code and artifact reference

[Overview](../README.md) · [Walkthrough](PROJECT_GUIDE.md) · [Development guide](DEVELOPMENT.md)

This reference describes the files on this branch. Function names are navigation aids; the walkthrough explains how their inputs, state, and outputs fit together.

## Python modules

### [scraper_producer.py](../Container_A/scraper_producer.py)

Optional bounded Selenium collection and durable RabbitMQ publishing.

- `findRedNotices(max_pages=1)`
- `send_to_rabbitmq(messages)`

### [consumer_db.py](../Container_B/consumer_db.py)

Validate queue messages, insert records transactionally, acknowledge after commit, and requeue database failures.

- `decode_notice(body)`
- `callback(channel, method, properties, body)`
- `main()`

### [database.py](../Container_B/database.py)

Create PostgreSQL connections from environment configuration.

- `connect()`

### [webapp.py](../Container_B/webapp.py)

Read the latest database records and render the Flask page.

- `definition()`

## Service and data artifacts

| Artifact | Responsibility |
| --- | --- |
| [docker-compose.yml](../docker-compose.yml) | Compose services, collection profile, startup dependencies, and loopback web exposure. |
| [database/schema.sql](../database/schema.sql) | Initial PostgreSQL table definition. |
| [.env.example](../.env.example) | Configuration variable names; copy locally and supply your own values. |

The stored row contains a generated ID plus name, age, and nationality. Queue payloads use `Name`, `Age`, and `Nationalities`; see the walkthrough for acknowledgement and duplicate-delivery behavior.

## Checks and setup

[Tests](../tests/) contains the focused checks described in the [development guide](DEVELOPMENT.md). Consult that guide for dependencies, commands, and the boundary between automated validation and untested integrations.
