import string, inspect

global file_name
file_name = "tags.tsv"

def createLists(file_name):
  tag=[]
  entity=[]

  count = max(enumerate(open(file_name)))[0]
  iterators = lineGenerator(file_name)

  try:
    for i in xrange(count):
      trans = string.maketrans('\t\n', '\t ')
      x= iterators.next()
      sep = string.translate(x, trans)
      sep = sep.split('\t')
      tag.append(sep[0])
      entity.append(sep[1])
  except StopIteration:
    pass

  return [entity, tag]

def lineGenerator(file_name):
  for line in open(file_name):
    yield line


print "\nContents of the Lists:\n "
#print "\n".join(str(i) for i in createLists(file_name))

'''
print "\nMethod to view the contents of the object:\n "
count = max(enumerate(open(file_name)))
print list(count) # Whenever you have to view object contents: use list function to call the contents of objects

'''
