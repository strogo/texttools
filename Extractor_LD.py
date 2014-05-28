from flask import request
from flask import Flask
from nltk.corpus import stopwords
import ast, string, json
import Dicts3 as D

# _____________________________________________________________________________________________________

class entity_Extractor(object):

  def __init__(self, file_name):
    self.file_name = file_name
    self.Mdict, self.uniqueTags = D.createMultiDict(file_name)
    # Mdict is the dictionary with keys as each word in the file_name and values as words appearing in the line.

  def extract(self, sentence):
    words = D.getWords(sentence)# Extract words from sentence: Stopwords removed, punctuations removed

    index, final = 0, []
    while index < len(words): # when index = length of list, it will end
      info, index = self.checkinDictionary( words,index,sentence)
      assert type(info) == list
      final = final + [a for a in info if a not in final]

    return getOutput(final)

  def checkinDictionary(self, words,index, sentence):
    j, position = index, sentence.find(words[index])+1

    if words[j] in self.Mdict:
      current_options = self.Mdict.getlist(words[j])
    else:
      return [], j+1

    if j == (len(words)-1):
      return [self.formatInput(an_option, position) for an_option in current_options], j+1
    else:
      flatten_listOfoptions = [word for i in current_options for word in i]
      while words[j+1] in flatten_listOfoptions:
        j, x = j + 1, 0
        new_options = [option for option in current_options if words[j] in option]
        current_options = new_options

        if j == (len(words)-1):
          break

    return self.getInfo(current_options, position), j+1

  def getInfo(self, final_options, position):
    info =[]
    for an_option in final_options:
      tag = list(set(an_option) & set(self.uniqueTags))[0]
      c = an_option.index(tag)
      info = info + [{'Entity' : " ".join(an_option[c+1:] + an_option[:c]), 'Tag': tag, 'Position': position }]
    return info
# _____________________________________________________________________________________________________
def getSentence():
  converted_list= request.form.copy().keys()[0]
  converted_dict=ast.literal_eval(converted_list)
  return converted_dict['sentence']

def getOutput(final):
  print "\n\t*Rule based entity search in progress...\n"

  if len(final)==0:
    return json.dumps({'Result' : "Entities not found", 'Search Results':  {}}), "\n"
  else:
    return json.dumps({'Result' : "Entities found",'Search Results' : final}, indent =4, sort_keys=False) + "\n"

# _____________________________________________________________________________________________________

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def process_request():
  if request.method == "POST":
    sentence= getSentence()
    return obj.extract(sentence)
  else:
    return "Only POST requests are accepted. No text found. Try Again...\n"

if __name__ == "__main__":
  file_name= "file.tsv"
  obj = entity_Extractor(file_name)
  app.debug=True
  app.run(host='0.0.0.0') #, use_reloader= False) # Without app.reloader it will run twice. and it will not debug
  # app.run(debug=True)
