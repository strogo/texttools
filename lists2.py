import string, inspect

def createLists(file_name):
  tag=[]
  entity=[]

  count = max(enumerate(open("file.tsv")))[0]
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

print "\nMethod to view the contents of the object:\n "
count = max(enumerate(open("file.tsv")))
print list(count) # Whenever you have to view object contents: use list function to call the contents of objects

print "\nContents of the Lists:\n "
print "\n".join(str(i) for i in createLists("file.tsv"))
