from collections import Counter
from nltk.tokenize import RegexpTokenizer
import yaml, json, os
from pathlib import Path

tokenizer = RegexpTokenizer(r'\w+')
analysis = {}

contractions = yaml.load(open('conf/contractions.yml', 'r'))

# Given a song's file name, count each word
def open_and_count(file_name):

	# read in a file, make it all lowercase
	# NAIVE implementation: case might matter in the future
	file = open('lyrics/%s.txt' % file_name, 'r').read().lower()

	# Replace contractions
	for contraction, replacement in contractions.items():
		file = file.replace(contraction, replacement)

	# Split words based off any non-alpha-numeric character
	text = tokenizer.tokenize(file)

	# Count occurrences of each word
	word_counts = dict(Counter(text))

	# Analysis on words
	analysis[file_name] = {}
	analysis[file_name]['total_words'] = len(text)
	analysis[file_name]['unique_words'] = len(word_counts)

	return word_counts

# Print each word and its count
def write_counts(words, file_name):
	new_path = 'analysis/%s.json' % file_name
	new_dir = file_name.split('/')[0] + '/'
	if not os.path.exists('analysis/' + new_dir):
		print('creating dir ' + new_dir)
		os.makedirs('analysis/' + new_dir)

	print('creating ' + new_path)
	file = open(new_path, 'w+')
	sorted_words = sorted(words.items(), key=lambda x:x[1], reverse=True)
	data_words = {w[0]: w[1] for w in sorted_words}
	data = {
		'data': {
			'words' : data_words
		}
	}
	print_analysis(file_name, data)

def print_analysis(file_name, data):
	
	percent_unique = str(round(100 *
		(analysis[file_name]['unique_words'] /
		analysis[file_name]['total_words']), 2)
	) + '%'
	analysis[file_name]['percent_unique'] = percent_unique

	data['data']['analysis'] = analysis[file_name]

	# Take all data and write it to file
	file = open('analysis/%s.json' % file_name, 'w+')
	file.write(json.dumps(data, indent=4))

def loop_through_files_and_analyze():
	pathlist = Path('lyrics/').glob('**/*.txt')
	for path_object in pathlist:

		# Because path is object, not string
		path = str(path_object).replace('lyrics/', '', 1) # Take out first occurrence
		path = path[:-4] # take off .txt
		print(path)

		words = open_and_count(path)
		write_counts(words, path)



# RUN HERE
loop_through_files_and_analyze()
