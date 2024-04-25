#!/bin/bash
sleep 10

service postgresql start

su postgres -c "psql -U postgres -c \"create database postgres_db;\""
su postgres -c "psql -U postgres -c \"alter user postgres password 'postgres';\""

python /app/consumer_db.py
wait

python /app/webapp.py

