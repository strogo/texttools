from flask import request
from flask import Flask
import flask
import ast
import re
import string

app=Flask(__name__)

@app.route("/", methods=["GET","POST"])
def extract():
  global lists
  global entities
  global tags

  lists = createLists("file.tsv")
  entities = lists[0]
  tags = lists[1]


  if request.method== "POST":
    sentence= getSentence()
    processed_sentence = stripSentence(sentence)
    words = processed_sentence.split() # gives list of words in sentence

    final = []

    for word in words:
      f = getInfo(word, entities, tags, sentence)
      if f!=None:
        final.append(f)
        print str(f)

    if len(final)==0:
      return "No Entity found."
    else:
      response = flask.make_response(getOutput(final))
      reponse.headers["content-type"] = "text/plain"
      return response#"Rule based entity search in progress...\n" + str(getOutput(final))

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

def getInfo(word, entity, tag, sentence):
#  pattern= r'\W*'+ word + r'\W*'
  pattern = '[^0-9A-Za-z]' + word + '[^0-9A-Za-z]'
  for x,single_entity in enumerate(entity):
    if re.search(pattern, single_entity):
      info = {"Entity" : single_entity, "Position" : sentence.find(word), "Tag" : tag[x]}
      return info

def createLists(file_name):
  tag=[]
  entity=[]

  with open(file_name) as f:
    lines = f.readlines()

  for line in lines:
    trans = string.maketrans('\t\n', '\t ')
    sep = string.translate(line, trans)
    sep = sep.split('\t')
    tag.append(sep[0])
    entity.append(sep[1])

  return [entity, tag]

def getOutput(final):
  print "Rule based entity search in process...\n"
  for i in final:
    print i


if __name__ == "__main__":
  app.debug=True
  app.run(host='0.0.0.0')
  # app.run(debug=True)
