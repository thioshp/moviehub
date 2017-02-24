import requests
from sys import exit
from console import *
from collections import OrderedDict
from pprint import pprint

def main():

	PROGRAM_WIDTH = 80 # Width of program
	API_URL = 'http://www.omdbapi.com/' # Open Movie Database API
	ROTTEN_TOMATOES = True # Show rotten tomatoes information
	FULL_PLOT = True # Show full plot

	printDivider(PROGRAM_WIDTH)
	print()
	print(centerAlignString('='*21, PROGRAM_WIDTH))
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
			exit(0)
		try:
			r = requests.get('http://www.omdbapi.com/', params=payload)
		except requests.exceptions.ConnectionError:
			print('Cannot establish connection to database.')
			exit(1)
		printDivider(PROGRAM_WIDTH)

		# Parse response
		if r.status_code == 200:
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
				heading = '\n%s (%s)' % (basicInfo['title'], basicInfo['year'])
				print(heading)
				print('-'*len(heading))
				print()
				for info in basicInfo.keys():
					if info == 'title' or info == 'year':
						continue
					print(info.upper())
					print()
					print(leftPadString(leftAlignString(basicInfo[info], PROGRAM_WIDTH-3), 3))
					print()

			else:
				print()
				print(res['Error'])
		else:
			print('Something went wrong: Error %s.' % r.status_code)
			printDivider(PROGRAM_WIDTH)
			exit(1)

if __name__ == '__main__':
  main()