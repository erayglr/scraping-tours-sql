import requests
import selectorlib
import os
import smtplib
import ssl
import time

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}



def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "erayguler5767@gmail.com"
    password = "kzoi iekn ynsk ixli"

    receiver = "erayguler5767@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

def store(extracted):
    with open("data.txt", "a") as file:
        if extracted not in read_data(file_local="data.txt"):
            file.write(extracted + "\n")


def read_data(file_local):
    with open(file_local, "r") as file:
        data = file.read()
    return data


if __name__ == "__main__":
    while True:
        if not os.path.exists("data.txt"):
            with open("data.txt", "w") as file:
                pass
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        if extracted != "No upcoming tours":
            if extracted not in read_data(file_local="data.txt"):
                store(extracted)
                send_email(message="Hey, new event was found")
        time.sleep(2)
