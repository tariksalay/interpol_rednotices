# Publish the queue stored in DB on web

import flask
import psycopg2
from datetime import datetime
import pytz # to get the time

# Initialize the Flask app
webapp = flask.Flask(__name__)

# Get the current time in the Turkey timezone
turkey_timezone = pytz.timezone('Europe/Istanbul')
current_time = datetime.now(tz=turkey_timezone).strftime("%Y-%m-%d %H:%M:%S")

# Establish connection to PostgreSQL
connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)

# Source: evieplus Academy Python - Flask 161/162
# https://www.youtube.com/watch?v=wUKb_LC23NM&list=PLtTs2BKyiS4DLNLTVJ1ZtapaCn5wtjI_k&index=3&ab_channel=evieplusAcademy

# Define a route for the index page
# "/" means the homepage (domain)
@webapp.route("/")
def definition():
    # Create a cursor for executing SQL commands
    cursor = connection.cursor()

    # Query the 'interpol_rednotices' table to pull all
    cursor.execute("SELECT * FROM interpol_rednotices LIMIT 20")
    data = cursor.fetchall()

    # Commit the transaction and close the cursor
    connection.commit()
    cursor.close()

    # Render the template from Directory created, and pass the data
    return flask.render_template("definition.html", data=data, current_time=current_time)

# Run the Flask app if this script is executed directly
if __name__ == "__main__":
    webapp.run(host='0.0.0.0', port=5000)
