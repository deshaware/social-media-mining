def main(arr):
    l,r = 0,len(arr) - 1
    print(r)
    result = [0] * len(arr)
    index = r
    while l <= r:
        if abs(arr[l]) < abs(arr[r]):
            result[index] = arr[r] * arr[r]
            r -= 1
        else:
            result[index] = arr[l] * arr[l]
            l += 1
        index -= 1
    return result

if __name__ == '__main__':
    print(main([-7,-3,2,3,11]))
    