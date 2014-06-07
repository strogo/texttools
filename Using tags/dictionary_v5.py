from werkzeug.datastructures import MultiDict as MD
from werkzeug.datastructures import TypeConversionDict as TCD
import string
from nltk.corpus import stopwords

global file_name, Mdict
file_name  = "file.tsv"

# _____________________________________________________________________________________________________

def lineGenerator(file_name):
  for line in open(file_name):
    yield line

def data():
  #Define global parameters
  global Mdict
  Mdict  = createMultiDict(file_name)
# _______________________________________Main Function______________________________________________________________

def createMultiDict(file_name):
  Mdict, uniqueTags = MD(), []
  count = max(enumerate(open(file_name)))[0]
  iterators = lineGenerator(file_name)

  try:
    for i in xrange(count):
      trans = string.maketrans('\n', '\t')# because there are \n characters on each line
      line = string.translate(iterators.next(), trans).split('\t')[:-1]
      line_words = list(set(getWords(line[1])).union(super_dict[line[1]]))
      if line[0] not in uniqueTags:
        uniqueTags = uniqueTags +[line[0]]
      for c in xrange(len(line_words)):
        Mdict.setlistdefault(line_words[c]).extend([[line_words ,line]])

  except StopIteration:
    pass

  return Mdict, uniqueTags

# _____________________________________________________________________________________________________

def stripSentence(sentence):
  #Create conversion table mapping punctuation and space to spaces
  trans= string.maketrans(string.punctuation + ' ',  ' '*33)
  #Strip sentence of its punctuations and replace those with spaces
  return sentence.translate(trans)

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


if __name__=="__main__" :
  data()
