import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader

BASE_URL = "http://quotes.toscrape.com"

def read_quotes(filename):
	with open(filename) as file:
		csv_reader = DictReader(file)
		return list(csv_reader)

def quote_game(all_quotes):
	quote = choice(all_quotes)
	print("Here's a quote: ")
	print(" ")
	print(quote["text"])
	print(" ")
	remaining_guesses = 4
	guess = ""
	while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
		guess = input(f"Who said this quote? Guesses remaining : {remaining_guesses} ")
		if guess.lower() == quote["author"].lower():
			print("Cheers! you got it right.")
			break
		remaining_guesses -= 1
		print_hint(quote, remaining_guesses)
	again = ""
	while again not in ('y','yes','n','no'):
		again = input("Would you like to play again (y/n)? ").lower()

	if again in ('y', 'yes'):
		print("Ok! playing the game again.")
		return quote_game(all_quotes)
	else:
		print("Ok! see you soon, goodbye!")

def print_hint(quote, remaining_guesses):
	if remaining_guesses == 3:
		res = requests.get(f"{BASE_URL}{quote['bio-link']}")
		author_soup = BeautifulSoup(res.text, "html.parser")
		birth_date = author_soup.find(class_="author-born-date").get_text()
		birth_location = author_soup.find(class_="author-born-location").get_text()
		print(f"Here's a hint: The author was born on {birth_date} {birth_location}")
	elif remaining_guesses == 2:
		print(f"Here's another hint: The author's first name starts with {quote['author'][0]}")
	elif remaining_guesses == 1:
		print(f"Here's last hint: The author's last name starts with {quote['author'].split(' ')[1][0]}")
	else:
		print(f"Sorry you ran out of guesses. The answer was {quote['author']}")
		print(" ")

quotes = read_quotes("quotes.csv")
quote_game(quotes)