from werkzeug.datastructures import MultiDict as MD
from werkzeug.datastructures import TypeConversionDict as TCD
import string
from nltk.corpus import stopwords

global file_name, Mdict
file_name  = "file.tsv"


def lineGenerator(file_name):
  for line in open(file_name):
    yield line

def data():
  #Define global parameters
  global Mdict
  Mdict  = createMultiDict(file_name)

def createMultiDict(file_name):
  Mdict, uniqueTags = MD(), []
  count = max(enumerate(open(file_name)))[0]
  iterators = lineGenerator(file_name)

  try:
    for i in xrange(count):
      trans = string.maketrans('\n', '\t')# because there are \n characters on each line
      line = string.translate(iterators.next(), trans).split('\t')
      tag, entity = line[0], line[1]

      if tag not in uniqueTags:
        uniqueTags = uniqueTags +[tag]
      entity = getWords(entity) # Extract words from sentence: Stopwords removed, punctuations removed
      # remove  "" from the list
      # remove ' ' from the list

      entity = [i for i in entity if entity!="" or entity!=" "]
      line_words = entity + [tag] # Words in a single line of the file
      for c in xrange(len(line_words)-1):
        Mdict.setlistdefault(line_words[c]).extend([line_words[c+1:] + line_words[:c] + [line_words[c]]])

  except StopIteration:
    pass

  return Mdict, uniqueTags

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


if __name__=="__main__" :
  data()
