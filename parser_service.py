import requests
from bs4 import BeautifulSoup
import pika


def parse_data_and_send_to_queue(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    person_name = soup.find('h1').get_text().strip()
    html_code = str(soup)

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='parsed_data_queue')

    message = f"{url}\n{person_name}\n{html_code}"
    channel.basic_publish(exchange='', routing_key='parsed_data_queue', body=message)

    print(f"Data for {url} sent to the queue")

    connection.close()


if __name__ == "__main__":
    url_to_parse = "https://career.habr.com/alishermadaminov9717"
    parse_data_and_send_to_queue(url_to_parse)
