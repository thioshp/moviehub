from distutils.core import setup

setup(
	name = 'moviehub',
	packages = ['moviehub'],
	install_requires = [
		'beautifulsoup4', 
		'requests'
	],
	version = '1.0.0',
	description = 'A console application for obtaining movie information using OMDb API',
	author = 'Marcus Mu',
	author_email = 'chunkhang@gmail.com',
	url = 'https://github.com/chunkhang/moviehub',
	download_url = 'https://github.com/chunkhang/moviehub/archive/1.0.0.tar.gz', 
	keywords = [
		'movie', 
		'hub', 
		'omdb'
	], 
	classifiers = [
		'Intended Audience :: End Users/Desktop',
		'Programming Language :: Python :: 3 :: Only',
		'Environment :: Console'
	],
	entry_points = [
		'console_scripts': [
			'moviehub=moviehub.moviehub:main'
		]
	]
)