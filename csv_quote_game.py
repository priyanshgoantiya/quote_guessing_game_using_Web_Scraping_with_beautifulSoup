from bs4 import BeautifulSoup
import requests
from time import sleep
from random import choice
import re
from csv import DictReader
base_url='https://quotes.toscrape.com/'

def read_quote(filename):
    with open(filename,'r',encoding='utf-8') as file:
        csv_reader=DictReader(file)
        return list(csv_reader)



def start_game(quotes):
    quote = choice(quotes)
    remaining_guesses = 5
    print("Here is the quote:")
    print(quote['text'])
    guess = ''

    while guess.lower() != quote['author'].lower() and remaining_guesses > 0:
        guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses}\n")
        if guess.lower() == quote['author'].lower():
            print("You got it correct!")
            break

        remaining_guesses -= 1

        if remaining_guesses == 4:
            res = requests.get(f"{base_url}{quote['About']}")
            soup = BeautifulSoup(res.text, 'html.parser')
            birth_date = soup.find(class_='author-born-date').get_text()
            birth_place = soup.find(class_='author-born-location').get_text()
            print(f"Here's a hint: The author was born in {birth_date} in {birth_place}")

        elif remaining_guesses == 3:
            res = requests.get(f"{base_url}{quote['About']}")
            soup = BeautifulSoup(res.text, 'html.parser')
            author_description = soup.find(class_='author-description').get_text()
            author_name = quote['author'].strip()
# Escape any special characters in the author's name
            escaped_author_name = re.escape(author_name)
# Replace the author's name with "$---" in the description
            updated_description = re.sub(escaped_author_name, "$---", author_description, flags=re.IGNORECASE)
            print(f"Another hint: {updated_description}")

        elif remaining_guesses == 2:
            author_name = quote['author']
            print(f"Another hint: The author's first name starts with: {author_name.split(' ')[0][0]}")

        elif remaining_guesses == 1:
            author_name = quote['author']
            last_initial = author_name.split(' ')[-1][0]  # Get the first letter of the last name
            print(f"The author's last name starts with: {last_initial}")

        else:
            print(f"Too many guesses! The author was: {quote['author']}")

    again = ''
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input("Would you like to play again (y,n)? ")

    if again.lower() in ('yes', 'y'):
        print("Ok, you can play again!")
        start_game(quotes)  # Restart the game
    else:
        print("Ok, goodbye!")

# Example call to start the game

quotes=read_quote("quotes.csv")
start_game(quotes)
