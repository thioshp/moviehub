import requests
from sys import exit
from console import *
from collections import OrderedDict
from pprint import pprint

def main():

	PROGRAM_NAME = 'OPEN MOVIE DATABASE'
	PROGRAM_WIDTH = 80 # Width of program
	API_URL = 'http://www.omdbapi.com/' # Open Movie Database API
	ROTTEN_TOMATOES = True # Show rotten tomatoes information
	FULL_PLOT = True # Show full plot

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
				print('Cannot establish connection to database.')
				input('Hit Enter to retry.')

		# Parse response
		if r.status_code == 200:
			print('Receiving information from database...')
			printDivider(PROGRAM_WIDTH)
			res = r.json()
			if res['Response'] == 'True':
				basicInfo = OrderedDict([
					('title', res['Title']),
					('year', res['Year']),
					('release date', res['Released']),
					('plot', res['Plot']),
					('director', res['Director']),
					('actors', res['Actors']),
					('writer', res['Writer']),
					('production', res['Production'])
				])		
				extraInfo = OrderedDict([
					('language', res['Language']),
					('genre', res['Genre']),
					('rated', res['Rated']),
					('runtime', res['Runtime']),
					('awards', res['Awards'])
				])			
				rottenTomatoesInfo = OrderedDict([
					('consensus', res['tomatoConsensus']),
					('percent', res['tomatoFresh']),
					('fresh', res['tomatoImage']),
					('rating', res['tomatoRating']),
					('url', res['tomatoURL'])
				])
				
				# Display information
				print()
				printHeader('%s (%s)' % (basicInfo['title'], basicInfo['year']))
				for info in basicInfo.keys():
					if info == 'title' or info == 'year':
						continue
					print(info.upper())
					print()
					print(leftPad(leftAlign(basicInfo[info], PROGRAM_WIDTH-3), 3))
					input()

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