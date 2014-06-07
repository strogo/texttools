import string
from nltk.corpus import stopwords

# _____________________________________________________________________________________________________

def stripSentence(sentence):
  #Create conversion table mapping punctuation and space to spaces
  trans= string.maketrans(string.punctuation + ' ',  ' '*33)
  #Strip sentence of its punctuations and replace those with spaces
  return sentence.translate(trans).replace("'s","")

def getStopwords():
  stops = stopwords.words('english')
  stops2 = [i[0].upper() + i[1:] for i in stops]
  return stops + stops2

def removeStopwords(words_with_stopwords):
  stop = getStopwords()
  words = [i for i in words_with_stopwords if i not in stop]
  return words

def getWords(sentence):
  processed_sentence = stripSentence(sentence)
  words_with_stopwords = processed_sentence.split() # gives list of words in sentence
  return removeStopwords(words_with_stopwords)
# _____________________________________________________________________________________________________
