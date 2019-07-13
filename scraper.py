import os
import requests
from bs4 import BeautifulSoup
from re import sub
from decimal import Decimal
import smtplib
import time
import colorama
from email.message import EmailMessage

URL = "https://www.amazon.com.au/Nintendo-Switch-Neon-Blue-Joy/dp/B01MUAGZ49/ref=sr_1_1?crid=3R8N" \
      "THQV05DTT&keywords=switch&qid=1562991615&s=gateway&sprefix=Switch%2Caps%2C360&sr=8-1"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/75.0.3770.100 Safari/537.36"
}

EMAIL = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']
DREAM_PRICE = 380


def check_price():
    # get request
    page = requests.get(URL, headers)
    # get page content
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        title = soup.find(id="productTitle").get_text().strip()
        price_str = soup.find(id="priceblock_ourprice").get_text()
        print(colorama.Fore.GREEN + time.ctime(),
              colorama.Fore.BLUE + title,
              colorama.Fore.CYAN + price_str)
        return Decimal(sub(r'[^\d.]', '', price_str))
    except:
        print(colorama.Fore.RED + time.ctime(), "Something went wrong")


def send_email():
    # Send the message via our own SMTP server.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(EMAIL, PASSWORD)

    # Edit email message
    msg = EmailMessage()
    msg['Subject'] = 'Price fell down!'
    msg['From'] = EMAIL
    msg['To'] = EMAIL
    msg.set_content(f'Check the amazon link {URL}')

    # send email
    server.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=msg.as_string())
    print("Message has been sent")

    # quit server
    server.quit()


while True:
    price = check_price()
    if price and price < DREAM_PRICE:
        send_email()
        break
    time.sleep(10)
