"""Open short-lived PostgreSQL connections using libpq environment variables."""
import psycopg2


def connect():
    # PGHOST, PGPORT, PGDATABASE, PGUSER and PGPASSWORD are supplied by Compose.
    return psycopg2.connect(connect_timeout=10)
