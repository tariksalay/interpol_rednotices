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
#WORKDIR /app
#?

# Reqs (from local file system,
# ADD/COPY
COPY reqs.txt /app/

# Install libraries
# Install Chrome Driver on Docker Container
RUN pip install -r /app/reqs.txt


RUN apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

RUN #-d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome:latest

# Copy app code
COPY scraper_producer.py /app/

# Run the app on the container terminal
CMD ["python", "/app/scraper_producer.py"]