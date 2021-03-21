inp = [2,4,6,7,1,-3]

obj = [(1,"swap",28), (2,"navu",22), (3,"chakshu",23)]

c = sorted(obj,key=lambda student: student[2])

print(c)