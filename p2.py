from flask import request
from flask import Flask
import flask, ast, re, string
from nltk.corpus import stopwords


global file_name, lists, entities, tags
file_name  = "tags.tsv"

def createLists(file_name):
  tag=[]
  entity=[]

  count = max(enumerate(open(file_name)))[0]
  iterators = lineGenerator(file_name)

  try:
    for i in xrange(count):
      trans = string.maketrans('\t\n', '\t ')
      sep = string.translate(iterators.next(), trans)
      sep = sep.split('\t')
      tag.append(sep[0])
      entity.append(sep[1])
  except StopIteration:
    pass

  return [entity, tag]

def lineGenerator(file_name):
  for line in open(file_name):
    yield line

def data():
  #Define global parameters
  global lists
  global entities
  global tags

  lists = createLists(file_name)
  entities = lists[0]
  tags = lists[1]

app=Flask(__name__)

def getOutput(final):
  print "\n\t*Rule based entity search in progress...\n"
  return "\nRule based entity search in progress...\n\n" + "\n".join(str(i) for i in final) + "\n\n"

@app.route("/", methods=["GET","POST"])
def extract():
  global lists
  global entities
  global tags


  if request.method== "POST":
    sentence= getSentence()
    processed_sentence = stripSentence(sentence)
    words_with_stopwords = processed_sentence.split() # gives list of words in sentence
    words = removeStopwords(words_with_stopwords)

    final = []

    for word in words:
      f = getInfo(word, entities, tags, sentence)
      if f!=None:
        final.append(f)

    if len(final)==0:
      return "No Entity found."
    else:
#      response = flask.make_response(getOutput(final))
#      reponse.headers["content-type"] = "text/plain"
      return getOutput(final)#"Rule based entity search in progress...\n" + str(getOutput(final))

  else:
    return "Only POST requests are accepted. No text found. Try Again...\n"


def getSentence():
  converted_list= request.form.copy().keys()[0]
  converted_dict=ast.literal_eval(converted_list)
  return converted_dict['sentence']

def stripSentence(sentence):
  #Create conversion table mapping punctuation and space to spaces
  trans= string.maketrans(string.punctuation + ' ',  ' '*33)
  #Strip sentence of its punctuations and replace those with spaces
  return sentence.translate(trans)

def removeStopwords(words_with_stopwords):
  stop = stopwords.words('english')
  words= []

  for i in words_with_stopwords:
    if i not in stop:
      words.append(i)
  return words


def getInfo(word, entity, tag, sentence):
#  pattern= r'\W*'+ word + r'\W*'
  pattern = '[^0-9A-Za-z]' + word + '[^0-9A-Za-z]'
  for x,single_entity in enumerate(entity):
    if re.search(pattern, single_entity):
      print pattern + "\n" + word
      info = {"Entity" : single_entity, "Position" : sentence.find(word), "Tag" : tag[x]}
      return info


if __name__ == "__main__":
  data()
  app.debug=True
  app.run(host='0.0.0.0') #, use_reloader= False) # Without app.reloader it will run twice. and it will not debug
  # app.run(debug=True)
