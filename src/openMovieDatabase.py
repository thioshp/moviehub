import sys
import requests
from pprint import pprint

def getChoice(numbers, choices, prompt='\nEnter choice: ', error='Invalid choice.'):
	'''
	Prompt user for choice
	Return an integer of valid choice
	'''
	assert len(numbers) == len(choices), 'Length of list of numbers and list of choices must be the same.'
	assert all(type(number) == int for number in numbers), 'Numbers must be integer.'
	assert all(type(choice) == str for choice in choices), 'Choices must be string.'
	for i in range(len(numbers)):
		print('(%s) %s' % (numbers[i], choices[i]))
	while True:
		choice = input(prompt)
		try:
			choice = int(choice)
			if choice in numbers:
				return choice
			else:
				raise ValueError()
		except ValueError:
			print(error)

def getQuery(prompt='\nEnter query: ', error='Invalid query.'):
	''' 
	Prompt user for query
	Return a string of valid query 
	'''
	while True:
		query = input(prompt)
		if query != '':
			return query
		else:
			print(error)

def printDivider(length, character='-', newLineAbove=True):
	''' Print a horizontal divider '''
	assert type(character) == str and len(character) == 1, 'Character must be string of length 1.'
	divider = character*length
	if newLineAbove:
		divider = '\n' + divider
	print(divider)

def leftAlignString(text, width):
	''' Return a string left-aligned within the given width '''
	words = text.split()
	# Check longest word against width
	longestWord = ''
	for word in words:
		if len(word) > len(longestWord):
			longestWord = word
	assert len(longestWord) <= width, 'Longest word cannot exceed width.'
	# Left-align text
	string = ''
	line = ''
	firstWord = True
	for word in words:
		lineLength = len(line)
		wordLength = len(word) + 1
		if firstWord:
			line += word
			firstWord = False
			continue
		if lineLength + wordLength > width:
			line += ('\n')
			string += line
			line = word
		else:
			line += (' ' + word)
	string += line
	return string

def centerAlignString(text, width):
	''' Return a string centered-aligned within the given width '''
	leftAlignedText = leftAlignString(text, width)
	lines = leftAlignedText.split('\n')
	centeredLines = list(map(lambda line: line.center(width), lines))
	return '\n'.join(centeredLines)

def main():

	PROGRAM_WIDTH = 50 # Width of program
	API_URL = 'http://www.omdbapi.com/' # Open Movie Database API
	ROTTEN_TOMATOES = True # Show rotten tomatoes information
	FULL_PLOT = True # Show full plot

	print()
	print(centerAlignString('OPEN MOVIE DATABASE', PROGRAM_WIDTH))
	print(centerAlignString('='*21, PROGRAM_WIDTH))
	print()

	while True:
		choice = getChoice([0, 1, 2], ['Instant', 'Search', 'Exit'])
		printDivider(PROGRAM_WIDTH)

		# Send request
		payload = {'tomatoes': 'true' if ROTTEN_TOMATOES else 'false', 'plot': 'full' if FULL_PLOT else 'short'}
		if choice == 0:
			payload['t'] = getQuery()
		elif choice == 1:
			payload['s'] = getQuery()
		else:
			sys.exit(0)
		try:
			r = requests.get('http://www.omdbapi.com/', params=payload)
		except requests.exceptions.ConnectionError:
			print('Cannot establish connection to database.')
			sys.exit(1)
		printDivider(PROGRAM_WIDTH)

		# Parse response
		if r.status_code == 200:
			res = r.json()
			if res['Response'] == 'True':
				# Basic information
				title = res['Title']
				released = res['Released']
				year = res['Year']
				genre = res['Genre']
				plot = res['Plot']
				director = res['Director']
				writer = res['Writer']
				actors = res['Actors']
				production = res['Production']

				# Extra information
				language = res['Language']
				rated = res['Rated']
				runtime = res['Runtime']
				awards = res['Awards']

				# Rotten Tomatoes information
				consensus = res['tomatoConsensus']
				percent = res['tomatoFresh']
				fresh = res['tomatoImage']
				rating = res['tomatoRating']
				url = res['tomatoURL']
				
				# Display information
				print()
				header = '%s (%s)' % (title, year)
				print(header)
				print('-'*len(header))
				print()

			else:
				print()
				print(res['Error'])
		else:
			print('Something went wrong: Error %s.' % r.status_code)
			printDivider(PROGRAM_WIDTH)
			sys.exit(1)

if __name__ == '__main__':
  main()