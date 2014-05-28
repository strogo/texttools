from flask import request
from flask import Flask
import flask, ast, re, string
from nltk.corpus import stopwords
import Dicts2, Dicts

global file_name, Mdict
file_name  = "file.tsv"

def main():
  global Mdict
  global uniqueTags

  f = Dicts2.createMultiDict(file_name)
  Mdict = f[0]
  uniqueTags = f[1]

app = Flask(__name__)

def getOutput(final):
  print "\n\t*Rule based entity search in progress...\n"
  return "\nRule based entity search in progress...\n\n" + "\n".join(str(i) for i in final) + "\n\n"

@app.route("/", methods=["GET","POST"])
def extract():
  global Mdict

  if request.method== "POST":
    sentence= getSentence()
    processed_sentence = stripSentence(sentence)
    words_with_stopwords = processed_sentence.split() # gives list of words in sentence
    words = removeStopwords(words_with_stopwords)

    final, index = [], 0
    while index < len(words): # when index = length of list, it will break
      l = checkinDictionary(words,index,sentence )
      index = l[1]

      if l[0] != None and l[0] != []:
        for a in l[0]:
          if a not in final:
            final.append(a)

    if len(final)==0:
      return "No Entity found.\n"
    else:
#      response = flask.make_response(getOutput(final))
#      reponse.headers["content-type"] = "text/plain"
      return getOutput(final)#"Rule based entity search in progress...\n" + str(getOutput(final))

  else:
    return "Only POST requests are accepted. No text found. Try Again...\n"


def checkinDictionary(words,index, sentence):
  global Mdict
  global uniqueTags
  j = index

  if words[j] in Mdict:
    W = Mdict.getlist(words[j])
  else:
    return [None, j+1]

  entity = words[j]


  while len(set(W) & set(uniqueTags)) != 0:
#  while W!=[]:
    print words, index, W, j, "\n"
    if j <= (len(words) -1):# and words[j+1] in W:
      j, W = j+1, Mdict.getlist(words[j+1])

    else:
      break
  # check for if W is not in the next words

  entity = " ".join(words[index:j])
  tags = list(set(W).intersection(set(uniqueTags)))

  info = []
  for x,tag in enumerate(tags):
#    print {'Entity' : entity, 'Position': sentence.find(words[index]) + 1, 'Tag' : tag}
    info.append({'Entity' : entity, 'Position': sentence.find(words[index]) + 1, 'Tag' : tag})

  return [info, j+1]


  # PSEUDOCODE:
  # j= index
  #   while (len(W) != len(W in uniqueTags))
  # if words[j+1] is in W : j++ and W = Mdict[words[j]] else check 2
  #      store: entity = entity + " " + words[j]
  # do above till there are only tags in W i.e.
  # for x,i in enumerate(W):
  #     make info as  a list i.e. info = []
  # info[x] = {'Entity' : entity, 'Position': sentence.find(words[index]), 'Tag' = i}
### back trace the word: Sani --> Abacha Sani so need to backtrace it. Entity and tags are mixed in it
  # return [info, j]

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
  stop2 =[]
  for i in stop:
    stop2.append(i[0].upper() + i[1:])
  stop = stop + stop2

  words= []

  for i in words_with_stopwords:
    if i not in stop:
      words.append(i)

  return words


if __name__ == "__main__":
  main()
  app.debug=True
  app.run(host='0.0.0.0') #, use_reloader= False) # Without app.reloader it will run twice. and it will not debug
  # app.run(debug=True)
