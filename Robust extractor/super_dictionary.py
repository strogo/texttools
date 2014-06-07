######only need to be done once
#read the text files line by line
#remove everything after pipe
#Get the canonical and form an entry in the dictionary
# key of that component:decompose variant into its components
#Everytime you get that canonical take the union of components of the variant
#super dictionry formed : dumpt it in string form
############################ MAKE SURE THE LAST LINE sepS WITH \n in the file
import re, json, string, progressbar, json
import sentence_manipulation as SM
from collections import defaultdict

# _____________________________________________________________________________________________________

class build_dictionary(object):

  def __init__(self, file_name, tag):
    self.file_name, self.tag = file_name, tag
    self.super_dictionary = {}

  def dictionary(self):
    iterators = lineGenerator(self.file_name)
    count = max(enumerate(open(self.file_name)))[0]
    try:
      for i in xrange(count):
        self.insert(iterators.next())
    except StopIteration:
      pass

    return self.super_dictionary

  def insert(self, x):
    if re.findall("__TG" , x):
      self.insertWithContext(x)
    elif re.findall("__COND", x):
      self.insertWithTopic(x)
    else:
      self.insertSimple(x)

  def insertRule(self, canonical, context, topic, variant):
    #print canonical
    if canonical not in self.super_dictionary :
      self.super_dictionary[canonical] = [ SM.getWords(variant), context, topic, self.tag ]
    else:
      C = self.super_dictionary[canonical]
      self.super_dictionary[canonical] = [ list( set(C[0]).union(set(SM.getWords(variant))) ), list( set(C[1]).union(set(context)) ), list( set(C[2]).union(set(topic))), self.tag  ]

  def insertSimple(self, x):
    canonical,  context, topic, variant = extractWithContext(x)
    self.insertRule(canonical, context, topic, variant)

  def insertWithContext(self, x):
    canonical, context, topic, variant = extractWithContext(x)
    self.insertRule(canonical, context, topic, variant)

  def insertWithTopic(self,x):
    canonicals, context, topics, variant = extractWithTopic(x)
    for i,canonical in enumerate(canonicals):
      self.insertRule(canonical, context, [topics[i]], variant)

# _____________________________________________________________________________________________________

def lineGenerator(file_name):
  for line in open(file_name):
    yield line

def extractWithContext(line):
  context_start, context_end  = re.search("__TG[^:]*:{\([^,]*", line), re.search("\)}:",line)
  if  not context_start:
    variant, line = line[ : line.find(',') ], line[ (line.find(",")+1) : ]
    canonical = processCanonical( line[ : line.find('|')], switch = 1 )
    return canonical, [], [], variant
  else:
    context = line[context_start.end() : context_end.start()]
    context = re.sub(r'(\([^,]*,)|(\))',"", context )
    context= [j for i in context.split(",") for j in i.replace("\"","").split(" ")]
    canonical = processCanonical(line[ (line.find(')}:')+3) : line.find('|') ] , switch =2)
    return canonical, context, [],  line[ : line.find(',__') ]

def processCanonical(canonical, switch):
  pattern_stripCanonical = "\(.*\)"
  canonical= re.sub(r'\\c', ',', canonical).replace(r'&#0038;',"&")
  if switch == 1 or switch == 2: # Normal or context
    canonical = re.sub( pattern_stripCanonical , "" , canonical).strip()
  else: # With topics
    canonical, pattern = canonical.replace("\"",""), re.compile(r'(\|)|($)')
    canonical = re.sub(pattern_stripCanonical, "" , canonical[: pattern.search(canonical).start()] ).strip()
  return canonical

def extractWithTopic(line):
  variant, line = line[ : line.find(',__') ], line[re.search(',__COND:', line).end() +1 :]
  topic, canonical, i, pattern = [], [], 0, re.compile(r'(\";)|($)')
  j, line, pos= line[  : pattern.search(line).end()+1], line[ pattern.search(line).end()+2 : ], 1
  while pos:
    tc= processTopicCanonicalPair(j)
    topic, canonical, pos = topic + [tc[0]], canonical + [tc[1]], pattern.search(line).end()
    j, line, i = line[ : pos+1] , line[pos+2 : ], i+1
  return canonical, [],  topic, variant

def processTopicCanonicalPair(pair):
  pair = pair.split("@")
  t,c = pair[0].replace("\"" , "") , processCanonical(pair[1], switch =3)
  return t,c

def combineDictionaries(list_of_dictionaries):
  super_dictionary={}
  for d in list_of_dictionaries:
    for k,v in d.iteritems():
      super_dictionary[k] = v
  return super_dictionary

# _____________________________________________________________________________________________________

def main():
  print "\nBuilding dictionaries..."

  bar = progressbar.ProgressBar(maxval=100, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
  bar.start()
  locations = build_dictionary("locations.txt", "nytd_geo").dictionary()
  bar.update(20)
  topics = build_dictionary("topics.txt", "nytd_topic").dictionary()
  bar.update(40)
  orgs = build_dictionary("org_all.txt", "nytd_org").dictionary()
  bar.update(60)
  porg = build_dictionary("porg.txt", "nytd_porg").dictionary()
  bar.update(80)
  persons = build_dictionary("persons.txt", "nytd_per").dictionary()
  bar.finish()
  print "Dictionaries ready to combine..."

  d1, d2, d3, d4, d5 = set(porg.keys()), set(locations.keys()), set(topics.keys()), set(orgs.keys()),  set(persons.keys()),
  intersections = [d1==d2, d1==d3, d1==d4, d1==d5, d2==d3, d2==d4, d2==d5,d3==d4,d3==d5,d4==d5]
  list_of_dictionaries = [porg, locations, topics, orgs, persons]

  if True not in intersections:
    print "No duplicate keys found in dictionaries...\nCombining dictionaries...\n"
    super_dictionary = combineDictionaries(list_of_dictionaries)
    print "Variant/Context/Topics dictionary created.\n"
  else:
    print "Dictionaries have duplicate keys. Please check your data or modify the code."

  return super_dictionary

# _____________________________________________________________________________________________________

if __name__=='__main__':
  SD = main()
  #SD = build_dictionary("locations.txt", "nytd_geo").dictionary()
  f= open('./super_dictionary.json', 'w+')
  json.dump(SD,f, ensure_ascii= False)
