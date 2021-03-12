
def calculate_depth(d, factor, count, ans):
    if d == ans or d + factor == ans:
        return count + 1
    elif (d + int(factor/2)) != ans:
        return calculate_depth(d + int(factor / 2), int(factor/2), count+1, ans)
    else:
        return count + 1

def depth6(depth):
    count = 0
    d = 1
    factor = 1
    count += 1
    while (d * 10) <= ans:
        d = d * 10
        factor = factor * 10
        count += 1

    count +=1 
    while (d + factor) < ans:
        d = d + factor
        count += 1
    return calculate_depth(d,factor,count,ans) 


def depth5(ans):
    count = 0
    d = 10
    fact = 10

    count += 1
    if d > ans:
        d = 1
    else:
        count += 1
        while (d * 10) < ans:
            d = d * 10
            fact = fact * 10
            count += 1

        count +=1 
        while (d + fact) < ans:
            d = d + fact
            count += 1
    
    if d + fact == ans:
        return count
    else:
        while d + fact != ans:
            if(d + int(fact/2)) < ans:
                count += 1
                fact = int(fact / 2)
                d = d + fact
            else:
                count += 1
                fact = int(fact / 2)
            
    return count + 1

def depth4(ans):
    count = 0
    d = 1
    fact = 1
    count += 1
    while (d * 10) <= ans:
        d = d * 10
        fact = fact * 10
        count += 1

    count +=1 
    while (d + fact) < ans:
        d = d + fact
        count += 1
    
    if d == ans or d + fact == ans:
        return count + 1
    else:
        while d + fact != ans:
            if(d + int(fact/2)) < ans:
                d = d + int(fact / 2)
            fact = int(fact / 2)
            count += 1
            
    return count + 1

def depth3(ans):
    count = 0
    d = 10
    fact = 10
    while True:
        if (d * 10) < ans:
            count += 1
            d = d * 10
            fact = fact * 10
        elif d > ans:
            d /= 10
            count += 1
            break
        elif (d + fact) < ans:
            count += 2
            d = d + fact
        else:
            count += 2
            break
    while d != ans:
        if d + fact == ans:
            count += 1
            break
        elif(d + int(fact/2)) < ans:
            count += 1
            fact = int(fact / 2)
            d = d + fact
        else:
            count += 2
            fact = int(fact / 2)
        
    return count + 1


def depth2(ans):
    count = 0
    d = 1
    fact = 1
    while True:
        if (d * 10) < ans:
            count += 1
            d = d * 10
            fact = fact * 10
        elif (d + fact) < ans:
            count += 2
            d = d + fact
        else:
            count += 2
            break

    while d != ans:
        if d + fact == ans:
            count += 1
            break
        elif(d + int(fact/2)) < ans:
            count += 1
            fact = int(fact / 2)
            d = d + fact
        else:
            count += 2
            fact = int(fact / 2)
        
    return count + 1
            




def depth(d, fact, count):
    count += 1
    if d == ans or d + fact == ans: # nor low no high
        return count + 1
    elif d + fact == ans:
        return count + 1
    elif (d * 10) <= ans:
        return depth(d * 10, d * 10, count + 1)
    elif (d + fact) < ans:
        return depth(d + fact, fact, count + 1)
    # elif (d + (fact / 2)) < ans:
    #     depth((d + (fact / 2)), fact / 2)
    fact = int(fact / 2)
    if (d + fact) > ans:
        return depth((d + int((fact / 2))), int(fact / 2), count + 1)
    else:
        return depth(d, int(fact / 2), count + 1)

def main():
    # measurement = depth(10,10,0)
    # print(measurement)
    ans2 = depth4(399)
    print(ans2)


ans = 301
count = 0
if __name__ == '__main__':
    main()
    