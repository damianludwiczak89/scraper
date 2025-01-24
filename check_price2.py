import requests
from bs4 import BeautifulSoup

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os

sender_email = "damian_konin@tlen.pl"
receiver_email = "olga_m922@tlen.pl"
password = os.getenv("EMAIL_PASSWORD")

url = 'https://www.zooplus.pl/shop/koty/drapaki_dla_kota/drapak_maly/100_cm/49253?activeVariant=49253.0'
result = requests.get(url)
page = BeautifulSoup(result.text, 'html.parser')
price = page.find('span', class_='z-price__amount z-price__amount--standard').text
price = float(price[:-3].replace(',', '.'))

message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email

if price < 109.96:
  message['Subject'] = f'CENA SŁUPKA SPADŁA!!!! Nowa cena: {price} zł!'
else:
  message['Subject'] = f'Cena słupka nie zmalała. Aktualna cena: {price} zł!'

body = 'https://www.zooplus.pl/shop/koty/drapaki_dla_kota/drapak_maly/100_cm/49253?activeVariant=49253.0'

message.attach(MIMEText(body, 'plain'))

try:
    with smtplib.SMTP('poczta.o2.pl', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email. Error: {e}")

