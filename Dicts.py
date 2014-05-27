from werkzeug.datastructures import MultiDict as MD
from werkzeug.datastructures import TypeConversionDict as TCD
import string
from nltk.corpus import stopwords

global file_name, Mdict
file_name  = "tags.tsv"


def lineGenerator(file_name):
  for line in open(file_name):
    yield line


def data():
  #Define global parameters
  global Mdict
  Mdict = createMultiDict(file_name)
  print "done", Mdict
def createMultiDict(file_name):
  Mdict = MD()

  count = max(enumerate(open(file_name)))[0]

  iterators = lineGenerator(file_name)

  stops = stopwords.words('english')
  stop2 =[]
  for i in stops:
    stop2.append(i[0].upper() + i[1:])
  stops = stops + stop2

  uniqueTags = []

  try:
    for i in xrange(count):
      trans = string.maketrans('\n', '\t')
      line = string.translate(iterators.next(), trans)
      line=line.split('\t')
      tag = line[0]

      entity=line[1]
      entity = stripSentence(entity) # remove punctuation
      entity = entity.split(' ')
      entity = removeStopwords(entity, stops) # remove stopwords

      # remove  " " from the list
      for i in xrange(entity.count("")):
        entity.remove("")
      # remove ' ' from the list
      for i in xrange(entity.count(" ")):
        entity.remove(" ")

      line = entity + [tag]

      if tag not in uniqueTags:
        uniqueTags.append(tag)

      for c in reversed(xrange(1,len(line))):
        Mdict.setlistdefault(line[c-1]).extend([line[c]])

  except StopIteration:
    pass

  return [Mdict, uniqueTags]

def stripSentence(sentence):
  #Create conversion table mapping punctuation and space to spaces
  trans= string.maketrans(string.punctuation + ' ',  ' '*33)
  #Strip sentence of its punctuations and replace those with spaces
  return sentence.translate(trans)

def removeStopwords(words_with_stopwords, stop):

  words= []

  for i in words_with_stopwords:
    if i not in stop:
      words.append(i)
  return words


if __name__=="__main__" :
  data()
