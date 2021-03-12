def depth(depth):
    count = 0
    d = 1
    fact = 1
    count += 1
    while (d * 10) <= depth:
        d = d * 10
        fact = fact * 10
        count += 1

    count +=1 
    while (d + fact) < depth:
        d = d + fact
        count += 1
    
    if d == depth or d + fact == depth:
        return count + 1
    else:
        while d + fact != depth:
            if(d + int(fact/2)) < depth:
                d = d + int(fact / 2)
            fact = int(fact / 2)
            count += 1
            
    return count + 1

if __name__ == '__main__':
    print(depth(301))
    