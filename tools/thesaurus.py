''' LEGACY COMPONENT
Early on during the project, I wanted to avoid having to shell out for a translation API by
attempting to create my own translation tool. The premise was that for each word in a message,
we would query a thesaurus API and replace the word with the first word in stored in the 
response JSON. The response would be an archaic and awkward, but still understandable "thesaurized" 
version of the same sentence. In fact, this goal was the inspiration for the project's first name: absurdspeak.
Of course words have drastically different synonymns depending on whether they're a  noun, verb, 
etc so the program returned rather crude translations. In the end, it become much for the scope of the project.
This will definitely be reworked outside the context of this project using nltk or something.
'''
import requests

ignored = ['a', 'the', 'this', 'that', 'will', 'there', 'they\'re', 'them' 'is', 'was', 'he', 'she', 'him', 'his' 'it', 'we', 'our', 'you', 'your', 'be', 'or', 'and', 'but', 'had', 'an', 'some', 'to', 'so', 'at', 'have', 'up', 'before', 'against', 'inside', 'by', 'beyond', 'on', 'past', 'prior', 'with', 'via', 'since']
def parse_word(msg):
	words = msg.split(' ')
	thesaurusized = list()
	# Access thesaurus API to replace word with first synonym
	for word in words:
		# Parse word for any trailing punctuation and strip it
		punctuation = [punctuation for punctuation in ['.', ',', ':', ';', '?'] if punctuation in word]
		mark = punctuation[0] if len(punctuation) != 0 else ''
		word = word.rstrip(mark)
		if word.lower() not in ignored:
			# Call API on word for synonyms
			response = requests.get(f"http://thesaurus.altervista.org/thesaurus/v1?key=Jrunb7M0IGjmy0SYlXs8&word={word}&language=en_US&output=json").json()
			if 'error' not in response:
				# Selecting and prettifying the first synonym obtained
				word = response['response'][0]['list']['synonyms'].split('|')[0]
				excluded = " (generic term)"
				if excluded in word:
					word = word[:word.find(excluded):]
			# Add any punctuation back
			word += mark
		thesaurusized.append(word)
	return ' '.join(thesaurusized)
# Tests
print(parse_word('You know I am not used to such ceremonies, and there was something ominous in the atmosphere.'))
