from bs4 import BeautifulSoup
import requests
from time import sleep
from random import choice
import re
from csv import DictWriter
import csv
base_url='https://quotes.toscrape.com/'
def scrap_quotes():
    all_quotes = []
    url = '/page/1'
    while url:
        res = requests.get(f"{base_url}{url}")
        # print(f"Now scraping{base_url}{url}...")
        soup = BeautifulSoup(res.text, 'html.parser')
        quotes = soup.find_all(class_='quote')


        for quote in quotes:
            all_quotes.append({"text": quote.find(class_='text').get_text(),
                               "author": quote.find(class_='author').get_text(),
                               "About": quote.find('a')["href"]})
        next_bnt = soup.find(class_='next')
        url = next_bnt.find('a')['href'] if next_bnt else None
    return all_quotes
quotes=scrap_quotes()
def write_quotes(quotes):
    with open('quotes.csv', 'w', encoding='utf-8') as file:
        header = ['text', 'author', 'About']
        csv_writer =DictWriter(file, fieldnames=header)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)
quotes=scrap_quotes()
write_quotes(quotes)


