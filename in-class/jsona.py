tel  = dict([('name','swapnil'),('age',28)])

import json
f = open('json.txt', 'w')
print(json.dumps(tel))

json.dump(tel,f)
f.close()

f = open('json.txt', 'r')
print(json.load(f))
f.close()