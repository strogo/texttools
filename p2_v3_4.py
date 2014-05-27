from flask import request
from flask import Flask
import flask, ast, re, string
from nltk.corpus import stopwords
import Dicts3 as D

global file_name, Mdict
file_name  = "file.tsv"

def main():
  global Mdict
  global uniqueTags

  f = D.createMultiDict(file_name)
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
    processed_sentence = D.stripSentence(sentence)
    words_with_stopwords = processed_sentence.split() # gives list of words in sentence
    words = D.removeStopwords(words_with_stopwords)

    final, index = [], 0
    while index < len(words): # when index = length of list, it will break
      l = checkinDictionary(words,index,sentence)
      print l, "A"
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
  j = index

  if words[j] in Mdict:
    current_lists = Mdict.getlist(words[j])
  else:
    return [None, j+1]

  if j == (len(words)-1):
    return [getInfo(current_lists, sentence.find(words[index])), j+1]
  else:
    while words[j+1] in sum_list(current_lists):
      j, x, new_lists = j + 1, 0, []

      for one_list in current_lists:
        if words[j] in one_list:
          new_lists.append(one_list)
      current_lists = new_lists

      if j == (len(words)-1):
        break

  info = getInfo(current_lists, sentence.find(words[index]))
  return [info, j+1]

def getInfo(lists, position):
  global uniqueTags
  info = []
  for x,i in enumerate(lists):
    tag = list(set(i) & set(uniqueTags))[0]
    c = i.index(tag)
    info.append({'Entity' : " ".join(i[c+1:] + i[:c]), 'Tag': tag, 'Position': position })
  return info

def sum_list(list_of_lists):
  out =[]
  for i in list_of_lists:
    out = out + i
  return out

def getSentence():
  converted_list= request.form.copy().keys()[0]
  converted_dict=ast.literal_eval(converted_list)
  return converted_dict['sentence']

if __name__ == "__main__":
  main()
  app.debug=True
  app.run(host='0.0.0.0') #, use_reloader= False) # Without app.reloader it will run twice. and it will not debug
  # app.run(debug=True)
