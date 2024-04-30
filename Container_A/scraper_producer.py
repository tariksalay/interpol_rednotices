import time
import pika
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities

# load up the options to change
options = Options()

# less secure, faster for development
options.add_argument("--headless")
options.add_argument("window-size=1920,1080")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--no-sandbox")
# overcome limited resource problems
options.add_argument("--disable-dev-shm-usage")



# scraping function , first page only
def findRedNotices():
    # start Chrome
    # go to redflag page
    url = "https://www.interpol.int/How-we-work/Notices/Red-Notices/View-Red-Notices/"
    driver = webdriver.Chrome(options=options)
    # go to the page
    driver.get(url)

    # load up the page
    time.sleep(2)
    # to store later
    red_notices_list = []

    # pull the name
    # names = driver.find_elements(By.CLASS_NAME, "redNoticeItem__labelLink")
    # pull the age
    # ages = driver.find_elements(By.CLASS_NAME, "age")
    # pull the nationality
    # nationalities = driver.find_elements(By.CLASS_NAME, "nationalities")
    # find the next element button
    nxt = driver.find_element(By.CLASS_NAME, "nextElement")
    # last page will be [] in the beginning
    # last_page = driver.find_elements(By.CLASS_NAME, "nextElement hidden")
    pg = 1
    i = 1
    right_arrow = driver.find_elements(By.CLASS_NAME, "nextIndex right-arrow")

    # go through the pages as long as there is a next page button and last_page button doesn't exist
    # while nxt && len(next_page) != 0::
    while not right_arrow:
        try:
            i += 1
            print(f"Pulling the names on Page {pg}")
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
            print("Finished pulling the data on this page")
            # scroll to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # click on the next page
            nxt.click()
            time.sleep(2)
            print(f"Page number {pg} have been successfully retrieved, going to the next page")
            pg += 1
            nxt = driver.find_element(By.CLASS_NAME, "nextElement")
            right_arrow = driver.find_elements(By.CLASS_NAME, "nextIndex right-arrow")
            # once went through all pages, next page button will disappear
        except:
            print("The last page has been retrieved.")
            break

    driver.quit()

    # return the list
    return red_notices_list


# Push red notices list to rabbitmq queue

def send_to_rabbitmq(message):
    # Connect to MQ
    connection_parameters = pika.ConnectionParameters('172.17.0.2')
    # connection_parameters = pika.ConnectionParameters('localhost')
    rabbitmq_connection = pika.BlockingConnection(connection_parameters)
    channel = rabbitmq_connection.channel()  # creates the channel

    # Declare a queue along with its name
    # Durable = true to make the queue survive a broker restart
    # durable=True for Docker
    channel.queue_declare(queue='red_notices_queue', durable=True)
    # channel.queue_declare(queue='red_notices_queue')
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
