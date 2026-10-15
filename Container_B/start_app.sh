#!/bin/sh
# PostgreSQL and the consumer now run as separate Compose services.
set -eu
exec gunicorn --bind 0.0.0.0:5000 --workers 2 webapp:webapp
