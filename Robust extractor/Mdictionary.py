from werkzeug.datastructures import MultiDict as MD
import string,json, ast
import numpy as np
from nltk.corpus import stopwords
import sentence_manipulation as SM

class build_Mdictionary(object):

  def __init__(self, file_name, super_dictionary_name):
    self.file_name, self.super_dictionary_name = file_name, super_dictionary_name
    self.Mdict, self.uniqueTags, self.super_dictionary= MD(), [],  {}

  def createMultiDict(self):
    print "Modifying the Master Dictionary with entries in Super Dictionary..."
    temp_d = self.MD_modified_by_SD()
    print "Appending the new entries in Super Dictionary to Multi Dictionary..."
    self.SD_appended_to_MD(temp_d)
    return self.Mdict, self.uniqueTags

  def MD_modified_by_SD(self):
    count, iterators = max(enumerate(open(self.file_name)))[0], lineGenerator(self.file_name)
    self.super_dictionary= ast.literal_eval(open(self.super_dictionary_name,"r").readline())
    trans, temp_d = string.maketrans('\n', '\t'), {}# because there are \n characters on each line

    try:
      for i in xrange(count):
        line = string.translate(iterators.next(), trans).split('\t')[:-1]
        lookup = self.super_dictionary[line[1]]
        temp_d[line[1]] = ""
        line_words = list(set(SM.getWords(line[1])).union(set(lookup[0])))
        if line[0] not in self.uniqueTags:
          self.uniqueTags = self.uniqueTags +[line[0]]
        for c in xrange(len(line_words)):
          self.Mdict.setlistdefault(line_words[c]).extend([[ line_words ,line, lookup[1], lookup[2] ]])

    except StopIteration:
      pass

    return temp_d

  def SD_appended_to_MD(self, temp_d):
    for k,v in self.super_dictionary.iteritems():
      if k not in temp_d:
        for c in xrange(len(v[0])):
          self.Mdict.setlistdefault(v[0][c]).extend([[ v[0] ,[v[3], k], v[1], v[2] ]])


# _____________________________________________________________________________________________________

def lineGenerator(file_name):
  for line in open(file_name):
    yield line

# _____________________________________________________________________________________________________


if __name__=="__main__" :
  e = build_Mdictionary("file.tsv", "super_dictionary.json")
  Mdict, uniqueTags = e.createMultiDict()
  f= open('./master_dictionary.json', 'w+')
  json.dump(Mdict,f, ensure_ascii= False)

  print "Multi-dictionary dumped to master_dictionary.json in the same directory."

  print "DONE"
