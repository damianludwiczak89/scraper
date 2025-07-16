from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

display = Display(visible=0, size=(800, 800))  
display.start()

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

chrome_options = webdriver.ChromeOptions()    
# Add your options as needed    
options = [
  # Define window size here
   "--window-size=1200,1200",
    "--ignore-certificate-errors"
 
    "--headless=new",
    #"--disable-gpu",
    #"--window-size=1920,1200",
    #"--ignore-certificate-errors",
    #"--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    '--remote-debugging-port=9222'
]

for option in options:
    chrome_options.add_argument(option)

sender_email = "damian_konin@tlen.pl"
receiver_emails = ["damian_konin@tlen.pl", "olga_m922@tlen.pl"]
password = os.getenv("EMAIL_PASSWORD")

links = [
   ['https://www.airbnb.pl/rooms/1110043269300501078?photo_id=1859810333&source_impression_id=p3_1752397905_P3ECu5IZ-5iMUATI&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26', 5416, 'airbnb'],
   ['https://www.airbnb.pl/rooms/1457230180563789971?photo_id=2242190329&source_impression_id=p3_1752397904_P3QTKep2EaRxFCf5&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26', 3642, 'airbnb'],
   ['https://www.airbnb.pl/rooms/31469942?photo_id=2121079081&source_impression_id=p3_1752397905_P3W0oIogPVAADBSM&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26', 4551, 'airbnb'], 
   ['https://www.airbnb.pl/rooms/14319489?photo_id=192184202&source_impression_id=p3_1752397905_P3qCz4w1RY71gGX-&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26', 4248, 'airbnb'],
   ['https://www.airbnb.pl/rooms/1137549188556102228?photo_id=1892606846&source_impression_id=p3_1752397905_P3-mGMiggbjyWpJd&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26', 4353, 'airbnb'],
   ['https://www.airbnb.pl/rooms/4223067?photo_id=119301402&source_impression_id=p3_1752397904_P3zZPwvCSpUbVjjp&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26', 3361, 'airbnb'],
   ['https://www.airbnb.pl/rooms/1110043269300501078?photo_id=1859810333&source_impression_id=p3_1752397905_P3ECu5IZ-5iMUATI&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26', 5416, 'airbnb'],
   ['https://www.airbnb.pl/rooms/1303533168913125082?photo_id=2088427312&source_impression_id=p3_1752397904_P3HElL7VddIy_mM7&check_in=2025-08-20&guests=2&adults=2&check_out=2025-08-26', 4468, 'airbnb'],
   ['https://www.booking.com/hotel/it/rome-dreamer-suite.pl.html?label=gen173nr-1BCAEoggI46AdIM1gEaLYBiAEBmAEeuAEXyAEP2AEB6AEBiAIBqAIDuAKw883DBsACAdICJGFkNDQyNjliLTZiMzktNGJjOS1iZjg3LTMwMjg1NjdjOTI2YdgCBeACAQ&sid=dd03763e9d4a20515107462032c4ee98&aid=304142&ucfs=1&checkin=2025-08-20&checkout=2025-08-26&dest_id=204&dest_type=district&group_adults=2&no_rooms=1&group_children=0&nflt=privacy_type%3D3%3Broomfacility%3D38%3Broomfacility%3D11%3Broomfacility%3D123%3Boos%3D1&srpvid=84c9da7d12b430321c47d11428cd804c&srepoch=1752398638&matching_block_id=1451470801_416501910_2_0_0&atlas_src=sr_iw_title#map_closed', 5767, 'booking'],
   ['https://www.booking.com/hotel/it/iflat-incredible-view-of-the-heart-of-rome-roma.pl.html?aid=356980&label=gog235jc-1FCAsocUIvaWZsYXQtaW5jcmVkaWJsZS12aWV3LW9mLXRoZS1oZWFydC1vZi1yb21lLXJvbWFIHlgDaLYBiAEBmAEeuAEXyAEP2AEB6AEB-AECiAIBqAIDuALavc7DBsACAdICJDhhYjliYTY0LTZmZjEtNGQwYS05NGQyLTdiZjc3YjZjODZjN9gCBeACAQ&sid=05e22aa2e7751b03e6abdaf20f6935fa&all_sr_blocks=885216801_413770714_0_0_0&checkin=2025-08-20&checkout=2025-08-26&dest_id=-126693&dest_type=city&dist=0&group_adults=2&group_children=0&hapos=1&highlighted_blocks=885216801_413770714_0_0_0&hpos=1&matching_block_id=885216801_413770714_0_0_0&no_rooms=1&req_adults=2&req_children=0&room1=A%2CA&sb_price_type=total&sr_order=popularity&sr_pri_blocks=885216801_413770714_0_0_0__132820&srepoch=1752407796&srpvid=0ef953f79d7608ab&type=total&ucfs=1', 5663, 'booking']
]

body = ""

for link in links:
    
  driver = webdriver.Chrome(options = chrome_options)
  driver.get(link[0])

  # Sometimes page does not load correctly, added a loop to try few times
  for _ in range(3):
    try:
      WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, '_j1kt73' if link[2]=='airbnb' else 'prco-valign-middle-helper')))
      break
    except TimeoutException:
      pass

  html = driver.page_source
  driver.quit()
  page = BeautifulSoup(html, 'html.parser')
  print(html)
  print()
  print(page)
  if link[2] == 'airbnb':
    price = [x.text.strip() for x in page.find_all('span', class_='_j1kt73') if 'zł' in x.text][0]
    price = int(price.replace('\xa0', '').split(',')[0])
  elif link[2] == 'booking':
    price = page.find_all('span', class_='prco-valign-middle-helper')
    print(link[0], '\n', price)
    price = min([
        x.text.strip()        
        .replace('\xa0', '')       
        .replace(' ', '')           
        .replace('zł', '')          
        for x in price
    ])

  body += f'\n - cena startowa {link[1]}, obecna cena - {price} -- {link[0]} \n\n'

message = MIMEMultipart()
message['From'] = sender_email
message['To'] = ", ".join(receiver_emails)

message['Subject'] = f'Ceny rzym'



message.attach(MIMEText(body, 'plain'))

try:
    with smtplib.SMTP('poczta.o2.pl', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_emails, text)
        print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email. Error: {e}")
