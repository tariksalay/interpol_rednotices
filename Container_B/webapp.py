"""Read-only local prototype UI. Importing the app does not open a database."""
from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, render_template
from database import connect

webapp = Flask(__name__)


@webapp.get('/')
def definition():
    connection = connect()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM interpol_rednotices ORDER BY id DESC LIMIT 1000')
                data = cursor.fetchall()
    finally:
        connection.close()
    current_time = datetime.now(ZoneInfo('Europe/Istanbul')).strftime('%Y-%m-%d %H:%M:%S')
    return render_template('definition.html', data=data, current_time=current_time)


if __name__ == '__main__':
    webapp.run(host='127.0.0.1', port=5000)
