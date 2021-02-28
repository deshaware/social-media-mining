tel  = dict([('name','swapnil'),('age',28)])

import _pickle
f = open('dump.pickle', 'wb')
_pickle.dump(tel,f)
f.close()

f = open('dump.pickle', 'rb')
data = _pickle.load(f)
print(data)
f.close()
