import re, string
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



sentence = "In conversation with International New York Times culture editor Julie Bloom, Piven talked about his experiences shooting in London, his theatrical background and his upcoming films the movie."

word =  " International"
pattern = '[^0-9A-Za-z]' + word + '[^0-9A-Za-z]'
data()

for single_entity in entities:
  x = re.finditer(pattern, single_entity)
  print " ".join([str(i.start(0)) for i in x])
