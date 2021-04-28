def merge(left, right):
    l, r = 0, 0
    result = []
    while l < len(left) and r < len(right):
        if left[l] <= right[r]:
            l += 1
            result.append(left[l])
        else:
            result.append(right[r])
            r += 1
    result += left[l:]
    result += right[r:]
    return result

def merge_sort(arr):
    if(len(arr) <= 1):
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


if __name__ == '__main__':
    print(merge_sort([5,4,3,1]))
    