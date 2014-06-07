from flask import request
from flask import Flask
from nltk.corpus import stopwords
import ast, string, json, itertools
import dictionary_v3 as Dict

# _____________________________________________OBJECT________________________________________________________

class entity_Extractor(object):

  def __init__(self, file_name):
    self.file_name = file_name
    print "Setting up server..."
    self.Mdict, self.uniqueTags = Dict.createMultiDict(file_name)
    # Mdict is the dictionary with keys as each word in the file_name and values as words appearing in the line.
    print "Server ready..."

  def extract(self, sentence):
    words = Dict.getWords(sentence)# Extract words from sentence: Stopwords removed, punctuations removed
    index, final = 0, []
    while index < len(words): # when index = length of list, it will end
      info, index = self.checkinDictionary( words,index,sentence)
      final = final + [a for a in info if a not in final]
    return getOutput(final)

  def checkinDictionary(self, words,index, sentence):
    j, position, new_options,new_entities = index, sentence.find(words[index])+1, [], []

    if words[j] in self.Mdict:
      options_list = self.Mdict.getlist(words[j])
      current_options, current_entities = [i[0] for i in options_list], [i[1] for i in options_list]
    else:
      return [], j+1

    if j == (len(words)-1):
      return self.getInfo(current_entities, position), j+1
    else:
      flatten_listOfoptions = [word for i in current_options for word in i]
      while words[j+1] in flatten_listOfoptions:
        j, x = j + 1, 0

        for x,y in itertools.izip(current_options, current_entities):
          new_options,new_entities = new_options+[x], new_entities+[y]
        current_entities= new_entities

        if j == (len(words)-1):
          break
    return self.getInfo(current_entities, position), j+1

  def getInfo(self, final_entities, position):
    info =[]
    for an_entity in final_entities:
      info = info + [{'Entity' : " ".join(an_entity[1:]), 'Tag': an_entity[0], 'Position': position }]
    return info
# ____________________________________________FUNCTIONS_________________________________________________________
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

# ______________________________________________APPLICATION_______________________________________________________

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def process_request():
  if request.method == "POST":
    sentence= getSentence()
    return obj.extract(sentence)
  else:
    return "Only POST requests are accepted. No text found. Try Again...\n"

# ___________________________________________________MAIN_______________________________________________________

if __name__ == "__main__":
  file_name= "file.tsv"
  obj = entity_Extractor(file_name)
  app.debug=True
  app.run(host='0.0.0.0') #, use_reloader= False) # Without app.reloader it will run twice. and it will not debug
  # app.run(debug=True)
