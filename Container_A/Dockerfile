FROM python:3.12-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 CHROME_BINARY=/usr/bin/chromium CHROMEDRIVER=/usr/bin/chromedriver
RUN apt-get update && apt-get install -y --no-install-recommends chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home collector
WORKDIR /app
COPY reqs.txt .
RUN pip install --no-cache-dir -r reqs.txt
COPY scraper_producer.py .
USER collector
CMD ["python", "scraper_producer.py"]
