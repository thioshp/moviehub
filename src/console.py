# Console is a module that provides common console operations

# PROMPTS
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

# STRING ADJUSTMENT
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

def leftPadString(text, padding):
	''' Return a string left-padded with the given padding '''
	lines = text.split('\n')
	paddedLines = (map(lambda line: ' '*padding + line, lines))
	return '\n'.join(paddedLines)

# STRUCTURING
def printDivider(length, character='-', newLineAbove=True):
	''' Print a horizontal divider '''
	assert type(character) == str and len(character) == 1, 'Character must be string of length 1.'
	divider = character*length
	if newLineAbove:
		divider = '\n' + divider
	print(divider)