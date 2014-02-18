import re, collections

#Spell Checker Starts
def dictwords(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

def known(words, dictonary): return set(w for w in words if w in dictonary)

def mywords(filename, splitter):
	lingoDict = {}
	with open(filename) as infile:
		for line in infile:
			line=line.strip();
			columns = line.split(splitter);
			word = columns[0];
			if len(columns)==2:
				meaning = columns[1]
			else:
				meaning = columns[0]
			lingoDict[word] = meaning.lower();
	return lingoDict		

alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word, dictonary):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in dictonary)	

DICTWORDS  = train(dictwords(file('dict.txt').read()))
HAPPYWORDS = train(dictwords(file('happy.txt').read()))
SADWORDS   = train(dictwords(file('sad.txt').read()))
LINGOWORDS = mywords('internet lingo.txt',":")
SLANGWORDS = mywords('slang.txt',":")
ABBREWORDS = mywords('abbreviation.txt',"@")
#~ EMOTICON   = mywords('emoticon.txt',"@#$%")

def correct_word(word):
	if known([word], DICTWORDS): #Word exists in online dictonary database
		return word
	elif known([word], LINGOWORDS.keys()): #Word exists in lingo dictonary made by us
		return LINGOWORDS[word]
	elif known([word], SLANGWORDS.keys()): #Slang shorthand db provided by http://www.noslang.com/dictionary
		return SLANGWORDS[word]
	elif known([word], HAPPYWORDS): 
		return "happy"
	elif known([word], SADWORDS): 
		return "sad"	
	elif known([word], ABBREWORDS.keys()): #Abbreviation db provided by http://www.webopedia.com/quick_ref/textmessageabbreviations.asp
		return ABBREWORDS[word]		
	else:
		candidates = known(edits1(word), DICTWORDS) or known(edits1(word), LINGOWORDS) or known_edits2(word,DICTWORDS) or known_edits2(word,LINGOWORDS) or [word]
		#print candidates
		return max(candidates, key=DICTWORDS.get)
#Spell Checker Ends

from nltk.stem.wordnet import *
stemmmer = WordNetStemmer()

def correct(word_list):
	text = "";
	processed_text = "";
	punctuation = re.compile(r'[.?!,":;#\']') 
	for word in word_list:
		word = punctuation.sub("", word); #Remove punctuation	
		if word != "":
			processed_word  = correct_word(word); #Correct misspelled words
			stemmed_word = stemmmer.lemmatize(processed_word); #Convert each word in its stem form
			stemmed_word = punctuation.sub("", stemmed_word); #Remove punctuation
		
			text 		   = ''.join([text,word,' ']);
			processed_text = ''.join([processed_text,stemmed_word,' ']);
	return text, processed_text
