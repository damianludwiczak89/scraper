from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup

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
 
    "--headless",
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

    
driver = webdriver.Chrome(options = chrome_options)

driver.get('https://www.mediaexpert.pl/komputery-i-tablety/laptopy-i-ultrabooki/laptopy/laptop-asus-vivobook-15x-k3504va-ma480w-15-6-oled-i7-1355u-16gb-ram-1tb-ssd-windows-11-home')
html = driver.page_source

driver.quit

page = BeautifulSoup(html, 'html.parser')

price = page.find('span', class_='whole')

print(price.text)

