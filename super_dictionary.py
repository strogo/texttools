######only need to be done once
#read the text files line by line
#remove everything after pipe
#Get the canonical and form an entry in the dictionary
# key of that component:decompose variant into its components
#Everytime you get that canonical take the union of components of the variant
#super dictionry formed : dumpt it in string form

# use it as it is
import re, json, string
import dictionary_v5 as Dict

def lineGenerator(file_name):
  for line in open(file_name):
    yield line

# For persons and topics
def extract(file_name):
  iterators = lineGenerator(file_name)
  count = max(enumerate(open(file_name)))[0]
  super_dictionary = {}

  try:
    for i in xrange(count):
      x = iterators.next() #x is line
      context, variant  = extractContext(x)[0], x[: x.find(',')]
      if __TG
        if not context and not topic:
          canonical = re.sub(r'\\c', ',' , x[ (x.find(',')+1) : x.find('|')] ) 
          canonical = re.sub( "[0-9()\-]" , "" , canonical).replace( " " , "" ).replace( "," , ", " )
        else:
          canonical = re.sub(r'\\c', ',' , x[ (x.find(')}:')+3) : x.find('|') ] )
          canonical = re.sub( "[0-9()\-]" , "" , canonical).replace( " " , "" ).replace( "," , ", " )

        if canonical in super_dictionary:
          C = super_dictionary[canonical]
          super_dictionary[canonical] = [ list( set(C[0]).union(set(Dict.getWords(variant))) ), list( set(C[1]).union(set(context)) ) ] 
        else:
          super_dictionary[canonical] = [Dict.getWords(variant), context]
          #super_dictionary = [list(set(super_dictionary[canonical]).union(set(Dict.getWords(variant)))) if canonical in super_dictionary else Dict.getWords(variant)]
      else:
        canonical, topic = getTopic(line)

  except StopIteration:
    pass

  return json.dumps({file_name : super_dictionary}, indent =4, sort_keys=False) + "\n"

def extractContext(line):
  context_start, context_end  = re.search("__TG[A-Z]*:{\([A-Z]*,", line), re.search("\)}:",line)
  if  not context_start:
    return []
  else:
    context = line[context_start.end() : context_end.start()].replace("(,","").replace(")","").replace("OR","").replace("AND","")
    context= [j for i in context.split(",") for j in i.replace("\"","").split(" ")]
    return context

def getTopic(line):
  topic_start, topic, canonical = re.search("__COND:", line), [], []
  j= line[ topic_start : line.find(";")].split("@")
  line = line[line.find(;): ]
  while line != None
    topic[i], canonical[i] = j[0].replace("\"" , "") , j[1][ : j[1].find('|') ]
    canonical = re.sub( "[0-9()\-]\r\n" , "" , canonical).replace( " " , "" ).replace( "," , ", " )
    j, line = line[:line.find(";")].split("@"), line[line.find(;): ]
  return topic, canonical


if __name__=='__main__':
  file_name ="test.txt"
  print extract(file_name)
