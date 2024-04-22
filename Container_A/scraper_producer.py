# Scrape Interpol Red List

from selenium import webdriver  # needed for scraping
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pika  # needed for rabbitmq

# from Container_A.producer import send_to_rabbitmq

chrome_options = Options()  # load up the options to change
chrome_options.add_argument("--no-sandbox")  # less secure, easier for development


# scraping function , first page only
def findRedNotices():
    browser = webdriver.Chrome(options=chrome_options)  # start chrome
    browser.get("https://www.interpol.int/How-we-work/Notices/Red-Notices/View-Red-Notices")  # go to redflag page

    time.sleep(2)  # give it 2 secs
    red_notices_list = []  # to store later

    names = browser.find_elements(By.CLASS_NAME, "redNoticeItem__labelLink")  # pull up the name
    ages = browser.find_elements(By.CLASS_NAME, "age")  # pull up the age
    nationalities = browser.find_elements(By.CLASS_NAME, "nationalities")  # pull up the nationality

    for name_element, age_element, nation_element in zip(names, ages, nationalities):  # $
        name = name_element.text.replace("\n", "")
        age = age_element.text
        nationality = nation_element.text
        red_notices_list.append({"Name": name, "Age": age, "Nationalities": nationality})

    browser.quit()

    return red_notices_list  # return the list


# Push red notices list to rabbitmq queue

def send_to_rabbitmq(message):
    # Connect to Container C (RabbitMQ queue)
    connection_parameters = pika.ConnectionParameters('localhost')
    rabbitmq_connection = pika.BlockingConnection(connection_parameters)
    channel = rabbitmq_connection.channel()  # creates the channel

    # Declare a queue along with its name
    # Durable = true to make the queue survive a broker restart
    # channel.queue_declare(queue='red_notices_queue', durable=True)
    channel.queue_declare(queue='red_notices_queue')
    print("Queue has been declared")

    # publish each item of data to the Container_C queue
    # message is the function parameter here, list of red notice people
    # basic_publish method pushes each person's data down to the queue
    for i in message:
        channel.basic_publish(exchange='',
                              routing_key='red_notices_queue',
                              body=str(i),
                              properties=pika.BasicProperties(
                                  delivery_mode=2,
                              ))

    print(f"The updated list of Red Notices below has been pushed to the queue: \n{message}")

    # to not leave connection hanging
    # connection/channel will be closed, but the queue will have the message stored
    rabbitmq_connection.close()


if __name__ == "__main__":
    # stores the red notices
    redNotices = findRedNotices()

    # send the red notices
    send_to_rabbitmq(redNotices)
