import requests
from sys import exit
from console import *
from collections import OrderedDict
from pprint import pprint

def main():

	PROGRAM_NAME = 'OPEN MOVIE DATABASE'
	PROGRAM_WIDTH = 80 # Width of program
	API_URL = 'http://www.omdbapi.com/' # Open Movie Database API
	FULL_PLOT = False # Display full plot in basic information
	ROTTEN_TOMATOES = True # Display rotten tomatoes information
	EXTRA_INFO = True # Display extra information
	
	printDivider(PROGRAM_WIDTH)
	print()
	printTitle(PROGRAM_NAME, PROGRAM_WIDTH)
	print()
	print(centerAlign('~ Powered by OMDb API ~', PROGRAM_WIDTH))
	print(centerAlign(API_URL[7:-1], PROGRAM_WIDTH))

	while True:
		print()
		printHeader('Home Menu')
		options = ['Instant', 'Search', 'Exit']
		choice = getChoice([0, 1, 2], options)
		printDivider(PROGRAM_WIDTH)

		# Send request
		payload = {'tomatoes': 'true' if ROTTEN_TOMATOES else 'false', 'plot': 'full' if FULL_PLOT else 'short'}
		if choice == 0:
			print()
			printHeader(options[choice], newLineBelow=False)
			payload['t'] = getQuery()
		elif choice == 1:
			print()
			printHeader(options[choice], newLineBelow=False)
			payload['s'] = getQuery()
		else:
			exit(0)
		while True:
			print('\nSending query to database...')
			try:
				r = requests.get(API_URL, params=payload)
				break
			except requests.exceptions.ConnectionError:
				print('Cannot establish connection to database.\n')
				hitEnter('retry')

		# Parse response
		if r.status_code == 200:
			print('Receiving information from database...')
			printDivider(PROGRAM_WIDTH)
			res = r.json()

			# Only allow movies
			if 'Type' in res.keys() and res['Type'] != 'movie':
				res['Response'] = 'False'
				res['Error'] = 'Only movies are allowed!'

			if res['Response'] == 'True':
				title = res['Title']
				year = res['Year']
				information = [
					# Basic information
					OrderedDict([
						('plot', res['Plot']),
						('director', res['Director']),
						('writer', res['Writer']),
						('actors', res['Actors'])
					])
				]
				if ROTTEN_TOMATOES:
					information.append(
						# Rotten Tomatoes information
						OrderedDict([
							('consensus', res['tomatoConsensus']),
							('tomatometer', res['tomatoMeter'] + '%'),
							('average rating', res['tomatoRating'] + '/10'),
							('url', res['tomatoURL'])
						])
					)
				if EXTRA_INFO:
					information.append(
						# Extra information	
						OrderedDict([
							('genre', res['Genre']),	
							('rated', res['Rated']),
							('runtime', res['Runtime']),
							('release date', res['Released'])
						])
					)

				# Display information
				print()
				printHeader('%s (%s)' % (title, year))
				for info in information:
					for key in info.keys():
						print(key.upper() + '\n')
						detail = info[key]
						if 'N/A' in detail:
							detail = '-'
						print(leftPad(leftAlign(detail, PROGRAM_WIDTH-3), 3))
						print()
					hitEnter()
					print()

			else:
				print()
				printHeader('Error')
				print(res['Error'])
				print()

			printDivider(PROGRAM_WIDTH, newLineAbove=False)

		else:
			print('Something went wrong: Error %s.' % r.status_code)
			printDivider(PROGRAM_WIDTH)
			exit(1)

if __name__ == '__main__':
	main()