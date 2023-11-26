import csv
import requests
from bs4 import BeautifulSoup


def habr_parse_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    person_name = soup.find('h1').get_text().strip()
    html_code = str(soup)

    print(url)
    print(person_name)
    print(html_code)


def parse_csv():
    with open('habr.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for row in reader:
            url = row[0]
            habr_parse_data(url)


parse_csv()
