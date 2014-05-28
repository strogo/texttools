from flask import request
from flask import Flask
import flask, ast, re, string, json
from nltk.corpus import stopwords
import Dicts3 as D

global file_name, Mdict
file_name  = "file.tsv"

def main():
  global Mdict
  global uniqueTags
  Mdict, uniqueTags = D.createMultiDict(file_name)
  print "Server ready...", Mdict.getlist('Sani')

app = Flask(__name__)

def getOutput(final):
  print "\n\t*Rule based entity search in progress...\n"

  if len(final)==0:
    return json.dumps({'Result' : "Entities not found", 'Search Results':  {}}), "\n"
  else:
    return json.dumps({'Result' : "Entities found",'Search Results' : final}, indent =4, sort_keys= False) + "\n"
  #  return "\nRule based entity search in progress...\n\n" + "\n".join(str(i) for i in final)+"\n"

@app.route("/", methods=["GET","POST"])
def extract():
  if request.method== "POST":
    sentence= getSentence()
    words = D.getWords(sentence)# Extract words from sentence: Stopwords removed, punctuations removed
    index, final = 0, []
    while index < len(words): # when index = length of list, it will end
      info, index = checkinDictionary(words,index,sentence)
      final = final + [a for a in info if a not in final]

    return getOutput(final)
  else:
    return "Only POST requests are accepted. No text found. Try Again...\n"

def checkinDictionary(words,index, sentence):
  global Mdict
  j, position = index, sentence.find(words[index])+1

  if words[j] in Mdict:
    current_options = Mdict.getlist(words[j])
  else:
    return [], j+1

  if j == (len(words)-1):
    return [formatInput(an_option, position) for an_option in current_options], j+1
  else:
    flatten_listOfoptions = [word for i in current_options for word in i]
    while words[j+1] in flatten_listOfoptions:
      j, x = j + 1, 0
      new_options = [option for option in current_options if words[j] in option]
      current_options = new_options
      if j == (len(words)-1):
        break

  return [formatInput(an_option, position) for an_option in current_options], j+1

def formatInput(an_option, position):
  global uniqueTags
  tag = list(set(an_option) & set(uniqueTags))[0]
  c = an_option.index(tag)
  return {'Entity' : " ".join(an_option[c+1:] + an_option[:c]), 'Tag': tag, 'Position': position }

def getSentence():
  converted_list= request.form.copy().keys()[0]
  converted_dict=ast.literal_eval(converted_list)
  return converted_dict['sentence']

if __name__ == "__main__":
  main()
  app.debug=True
  app.run(host='0.0.0.0') #, use_reloader= False) # Without app.reloader it will run twice. and it will not debug
  # app.run(debug=True)
