from werkzeug.datastructures import MultiDict as MD
from werkzeug.datastructures import TypeConversionDict as TCD
import string, progressbar, json, ast
from nltk.corpus import stopwords
import sentence_manipulation as SM
import super_dictionary as SD
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
  super_dictionary= ast.literal_eval(open("super_dictionary.json","r").readline())
  bar = progressbar.ProgressBar(maxval= count, \
    widgets=[progressbar.Bar(':', '[', ']'), ' ', progressbar.Percentage()])
    #Variant #Context #Topic  #Tag
  try:
    for i in xrange(count):
      trans = string.maketrans('\n', '\t')# because there are \n characters on each line
      line = string.translate(iterators.next(), trans).split('\t')[:-1]
      lookup = super_dictionary[line[1]]
      line_words = list(set(SM.getWords(line[1])).union(set(lookup[0])))
      if line[0] not in uniqueTags:
        uniqueTags = uniqueTags +[line[0]]
      for c in xrange(len(line_words)):
        Mdict.setlistdefault(line_words[c]).extend([[ line_words ,line, lookup[1], lookup[2] ]])
      bar.update(i+1)
    bar.finish()
  except StopIteration:
    pass


  return Mdict, uniqueTags

# _____________________________________________________________________________________________________


if __name__=="__main__" :
  data()
