import string
def createLists(file_name):
  tag=[]
  entity=[]

  with open(file_name) as f:
    lines = f.readlines()
    print lines
    
  for line in lines:
    trans = string.maketrans('\t\n', '\t ')
    s =string.translate(line, trans)
    sep = s.split('\t')
    print sep
    tag.append(sep[0])
    entity.append(sep[1])

  return [entity, tag]

print createLists("file.tsv")
