import time
import pika
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# load up the options to change
options = Options()

options.add_argument("--headless")
# # less secure/faster for development, some needed for Docker
options.add_argument("--no-sandbox")
# overcome limited resource problems
options.add_argument("--disable-dev-shm-usage")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')


# scraping function , first page only
def findRedNotices():
    # start Chrome
    # go to redflag page
    url = "https://www.interpol.int/How-we-work/Notices/Red-Notices/View-Red-Notices/"
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    # driver = seleniumbase.Driver(browser="chrome", headless=False)
    # url = "https://www.interpol.int/How-we-work/Notices/Red-Notices/View-Red-Notices/"
    # driver.get(url)

    # give it 2 secs
    time.sleep(1)
    # to store later
    red_notices_list = []

    # pull the name
    names = driver.find_elements(By.CLASS_NAME, "redNoticeItem__labelLink")
    # pull the age
    ages = driver.find_elements(By.CLASS_NAME, "age")
    # pull the nationality
    nationalities = driver.find_elements(By.CLASS_NAME, "nationalities")

    for name_element, age_element, nation_element in zip(names, ages, nationalities):
        name = name_element.text.replace("\n", "")
        age = age_element.text
        nationality = nation_element.text
        red_notices_list.append({"Name": name, "Age": age, "Nationalities": nationality})

    driver.quit()

    # return the list
    return red_notices_list


# Push red notices list to rabbitmq queue

def send_to_rabbitmq(message):
    # Connect to Container C (RabbitMQ queue)
    connection_parameters = pika.ConnectionParameters('172.17.0.2')
    # connection_parameters = pika.ConnectionParameters('localhost')
    rabbitmq_connection = pika.BlockingConnection(connection_parameters)
    channel = rabbitmq_connection.channel()  # creates the channel

    # Declare a queue along with its name
    # Durable = true to make the queue survive a broker restart
    channel.queue_declare(queue='red_notices_queue', durable=True)
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
