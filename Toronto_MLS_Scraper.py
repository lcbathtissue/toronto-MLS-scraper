import csv
import os, time
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

headless = True
DEFAULT_DELAY = 3

class listing:
    def __init__(self):
        self.realtor_name = None
        self.phone_num = None
        self.listing_price = None
        self.listing_URL = None
    def set_realtor_name(self, realtor_name):
        self.realtor_name = realtor_name
    def set_phone_num(self, phone_num):
        self.phone_num = phone_num
    def set_listing_price(self, listing_price):
        self.listing_price = listing_price
    def set_listing_URL(self, listing_URL):
        self.listing_URL = listing_URL
    def set_listing_address(self, listing_address):
        self.listing_address = listing_address
    def get_realtor_name(self):
        return self.realtor_name
    def get_phone_num(self):
        return self.phone_num
    def get_listing_price(self):
        return self.listing_price
    def get_listing_URL(self):
        return self.listing_URL
    def get_listing_address(self):
        return self.listing_address

f = open("URLs.txt", "r")
URLS = f.read().split("\n")

load_dotenv()
user_name = os.getenv('USER_NAME')
pass_word = os.getenv('PASS_WORD')

seleBrowserPath = "C:\Program Files (x86)\chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument("--headless")
if (headless == True):
    seleDriver = webdriver.Chrome(seleBrowserPath, options=chrome_options)
else:
    seleDriver = webdriver.Chrome(seleBrowserPath)
seleDriver.get("https://collab.torontomls.net/signin")
time.sleep(DEFAULT_DELAY)
seleLink = seleDriver.find_element_by_id("username")
seleLink.send_keys(user_name)
seleLink = seleDriver.find_element_by_id("password")
seleLink.send_keys(pass_word)
seleLink = seleDriver.find_element_by_xpath('/html/body/div[1]/div[2]/form[3]/input')
seleLink.click()
time.sleep(DEFAULT_DELAY)

output_list = []
for index, URL in enumerate(URLS):
    print(f"[{index+1}] Scraping {URL}.. ", end="")
    seleDriver.get(URL)
    time.sleep(DEFAULT_DELAY)
    page_contents = str(seleDriver.page_source.encode('utf-8'))
    soup = BeautifulSoup(page_contents, features="lxml")
    price = str(soup.find("span", {"style": "color:darkblue"}).encode_contents())[3:-1]
    price = float(price.replace(",",""))
    address = str(soup.find("div", {"class": "addr"}).encode_contents())
    address = address[address.find("<h1> ")+len("<h1> "):address.find("</h1>")]
    contractor_DIV = str(soup.find("div", {"class": "sub-section"}).encode_contents())
    realtor = contractor_DIV[contractor_DIV.find("Listing Contracted With</span>")+len("Listing Contracted With</span>"):]
    realtor = realtor[27:realtor.find("</span>")]
    phone = contractor_DIV[contractor_DIV.find('<span class="phone">')+len('<span class="phone">'):]
    phone = phone[:phone.find("</span>")]
    print(f"{address} complete..")

    output_list.append(listing())
    listings_index = len(output_list) - 1
    output_list[listings_index].set_realtor_name(realtor)
    output_list[listings_index].set_phone_num(phone)
    output_list[listings_index].set_listing_price(price)
    output_list[listings_index].set_listing_URL(URL)
    output_list[listings_index].set_listing_address(address)

for listed_property in output_list:
    realtor = listed_property.get_realtor_name()
    phone = listed_property.get_phone_num()
    price = listed_property.get_listing_price()
    URL = listed_property.get_listing_URL()
    address = listed_property.get_listing_address()

    print(f"[{address}]: {URL}")
    with open('output.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow([address, f'=HYPERLINK("{URL}")', realtor, phone, price])
    csvfile.close()
