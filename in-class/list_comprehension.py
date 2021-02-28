fruit = [' banana', 'apple      ', 'pap   ayaa']
print([lol.strip() for lol in fruit])


print([3*x for x in range(1,5) if x > 2])

vec1 = [2,3,4]
vec2 = [4,3,-9]

print([x * y for x in vec1 for y in vec2])

#Dictionary Comprehension
print("======dict comprehension")
print({k: k*k for k in range(10)})

team = ['Arsenal', 'Chelsea', 'Liverpool']
print({k:v for k,v in enumerate(team)})

d = {1: ('regular mushroom pizza', 9.98), 2: ('medium chicken pizza', 9.98)}
for i,j in d.items():
    print(j)



