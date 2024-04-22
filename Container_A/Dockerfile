#FROM ubuntu:latest
#LABEL authors="Tarik Salay"
#
#ENTRYPOINT ["top", "-b"]

# Dockerfile: Blueprint to create the image
# There are images ready to use in DockerHub for common services such as PostgreSQL etc.
# Since this is my app I need to write the image

# Image (Base) : Recipe for container
FROM python:3.12.2

# Directory (Where to copy in Docker Container)
WORKDIR /PycharmProjects/tarik/Container_A

# Reqs (from local file system,
# ADD/COPY
COPY reqs.txt /app/

# Install dependencies
RUN pip install -r /app/reqs.txt
#RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
#RUN echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
#RUN apt-get update
#RUN apt-get install -y google-chrome-stable

# Copy app code
COPY scraper_producer.py /app/

# Run the app on the container terminal
CMD ["python", "/app/scraper_producer.py"]