"""Bounded, explicit collection of public notices followed by JSON publication."""
import json
import logging
import os

import pika
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = 'https://www.interpol.int/How-we-work/Notices/Red-Notices/View-Red-Notices/'
QUEUE = 'red_notices_queue'
LOGGER = logging.getLogger(__name__)


def findRedNotices(max_pages=1):
    if max_pages < 1:
        raise ValueError('max_pages must be positive')
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    # This is opt-in; do not disable Chrome sandbox protection by default.
    if os.getenv('CHROME_NO_SANDBOX') == '1':
        options.add_argument('--no-sandbox')
    if os.getenv('CHROME_BINARY'):
        options.binary_location = os.environ['CHROME_BINARY']
    service = Service(executable_path=os.environ['CHROMEDRIVER']) if os.getenv('CHROMEDRIVER') else Service()
    driver = webdriver.Chrome(options=options, service=service)
    notices = []
    try:
        driver.set_page_load_timeout(30)
        driver.get(URL)
        wait = WebDriverWait(driver, 15)
        previous = None
        for _ in range(max_pages):
            names = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'redNoticeItem__labelLink')))
            ages = driver.find_elements(By.CLASS_NAME, 'age')
            nations = driver.find_elements(By.CLASS_NAME, 'nationalities')
            if not (len(names) == len(ages) == len(nations)):
                raise RuntimeError('Notice markup changed: field counts do not match')
            page = [(n.text.replace('\n', ' ').strip(), a.text, country.text)
                    for n, a, country in zip(names, ages, nations)]
            if not page or page == previous:
                break
            notices.extend(dict(zip(('Name', 'Age', 'Nationalities'), record)) for record in page)
            previous = page
            if len(notices) and _ + 1 < max_pages:
                buttons = driver.find_elements(By.CSS_SELECTOR, '.nextElement:not(.hidden)')
                if not buttons or not buttons[0].is_displayed() or not buttons[0].is_enabled():
                    break
                first_name = names[0]
                buttons[0].click()
                # If navigation does not replace the results, report the timeout instead of duplicating a page.
                wait.until(EC.staleness_of(first_name))
        return notices
    finally:
        driver.quit()


def send_to_rabbitmq(messages):
    connection = pika.BlockingConnection(pika.URLParameters(os.environ['AMQP_URL']))
    try:
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE, durable=True)
        channel.confirm_delivery()
        for notice in messages:
            channel.basic_publish(exchange='', routing_key=QUEUE,
                                  body=json.dumps(notice, ensure_ascii=False).encode('utf-8'),
                                  mandatory=True, properties=pika.BasicProperties(
                                      delivery_mode=2, content_type='application/json'))
        LOGGER.info('Published %d notice records', len(messages))
    finally:
        connection.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    send_to_rabbitmq(findRedNotices(int(os.getenv('MAX_PAGES', '1'))))
