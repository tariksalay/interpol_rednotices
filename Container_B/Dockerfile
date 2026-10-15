FROM python:3.12-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY reqs.txt .
RUN pip install --no-cache-dir -r reqs.txt && useradd --create-home appuser
COPY consumer_db.py database.py webapp.py ./
COPY templates ./templates
USER appuser
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "webapp:webapp"]
