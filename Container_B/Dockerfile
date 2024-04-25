#FROM ubuntu:latest
#LABEL authors="Tarik Salay"
#
#ENTRYPOINT ["top", "-b"]

# Dockerfile to create the image
# There are images ready to use in DockerHub for common services such as PostgreSQL etc.

# Base image
FROM python:3.12.2

# Set working directory
WORKDIR /app

# Copy reqs
COPY reqs.txt /app/

# Install libraries
RUN pip install -r /app/reqs.txt

# Install PostgreSQL
RUN apt update && apt install -y postgresql postgresql-contrib

# Copy the codes
COPY consumer_db.py /app/
COPY webapp.py /app/
COPY templates/definition.html /app/templates/
COPY start_app.sh /app/
COPY pg_hba.conf ../etc/postgresql/16/main/pg_hba.conf

# Start the shell script
# chmod = change mode (permission)
RUN chmod +x /app/start_app.sh

# Expose port for the server
EXPOSE 5000

# Run the application
CMD ["/app/start_app.sh"]