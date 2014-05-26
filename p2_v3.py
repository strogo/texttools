from flask import request
from flask import Flask
import flask, ast, re, string
from nltk.corpus import stopwords
import Dicts

global file_name, Mdict
file_name  = "tags.tsv"

def main():
  global Mdict
  global uniqueTags

  f = Dicts.createMultiDict(file_name)
  Mdict = f[0]
  uniqueTags = f[1]

app=Flask(__name__)

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

    final = []

    while index < len(words): # when index = length of list, it will break
      l = checkinDictionary(words,index,sentence )



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

  entity = ""
  while len(set(W) & set(uniqueTags)) != 0:
    if words[j+1] in W:
      j, W = j+1, Mdict.getlist(words[j+1])
      entity = entity + words[j] + " "

  tags = set(W).intersection(set(uniqueTags))

  info = []
  for x,tag in enumerate(tags):
    info[x] = {'Entity' : entity, 'Position': sentence.find(words[index]), 'Tag' : tag}

  return info


  # PSEUDOCODE:
  # j= index
  #   while (len(W) != len(W in uniqueTags))
  # if words[j+1] is in W : j++ and W = Mdict[words[j]] else check 2
  #      store: entity = entity + " " + words[j]
  # do above till there are only tags in W i.e.
  # for x,i in enumerate(W):
  #     make info as  a list i.e. info = []
  # info[x] = {'Entity' : entity, 'Position': sentence.find(words[index]), 'Tag' = i}
  # back trace the word: Sani --> Abacha Sani so need to backtrace it. Entity and tags are mixed in it
  # return [info, j]




  return [index, info]

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


def getInfo(words, index, entity, tag, sentence, pattern):
  info, count, max_intersect = {}, 0,0

  for x,single_entity in enumerate(entity):
      if re.search(pattern, single_entity) != None:
        j = confirmEntity(words, index , single_entity, tags, x )
        condition = j[0]
        intersect = j[1]

        if max_intersect <= intersect :
          max_intersect = intersect
          info[count] = {"intersect":intersect ,"Entity" : single_entity, "Position" : sentence.find(words[index])+1, "Tag" : tag[x]}
          count = count + 1

#  for i in info:
#    if info[i]['intersect'] == max_intersect :
#      info[count] = {"Entity" : info[i]['Entity'], "Position" : info[i]['Position'], "Tag" : info[i]["Tag"]}
#      count = count + 1
  print count
  info = {"Word": words[index],"Entity" : info[count-1]['Entity'], "Position" : info[count-1]['Position'], "Tag" : info[count-1]['Tag']}

  if count == 0:
    return None
  else:
    return info

def confirmEntity(words, index, single_entity, tags, x):
  stripped_entity = stripSentence(single_entity)
  entity_with_stopwords = stripped_entity.split() # gives list of words in sentence
  entity_list = removeStopwords(entity_with_stopwords)

  index = 1 if index == 0 else index

  intersection = set([None if index else words[index-1],words[index],words[index+1]]).intersection(set(entity_list))

  if len(intersection) >= 1:
#    print index, str(set([words[index-1], words[index+1]])) + str(set(entity_list))
    return [True, len(intersection) - 1]
  else:
    return [False, 0]

if __name__ == "__main__":
  main()
  app.debug=True
  app.run(host='0.0.0.0') #, use_reloader= False) # Without app.reloader it will run twice. and it will not debug
  # app.run(debug=True)
