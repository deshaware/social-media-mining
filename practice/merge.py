def merge(left, right):
    """Merge sort merging function."""

    left_index, right_index = 0, 0
    result = []
    while left_index < len(left) and right_index < len(right):
        
        if left[left_index] <= right[right_index]:
            result.append(left[left_index])
            left_index += 1
        else:
            # if left[left_index] == right[right_index] and left[left_index] not in temp:
            #         temp.append(left[left_index])
            print("lenlef",len(left)+ 1 - left_index )
            temp2 = (len(left) - left_index) + 1
            temp.append(temp2)
            result.append(right[right_index])
            right_index += 1

    result += left[left_index:]
    result += right[right_index:]
    print("temp", len(temp))
    # print(inversion_count)
    return result

temp = list()
inversion_count = 0
def merge_sort(array):
    """Merge sort algorithm implementation."""
    
    if len(array) <= 1:  # base case
        return array

    # divide array in half and merge sort recursively
    half = len(array) // 2
    left = merge_sort(array[:half])
    right = merge_sort(array[half:])

    return merge(left, right)


if __name__ == '__main__':
    print(merge_sort([ 5,1,2,4,3]))
    # print(merge_sort([ 1, 9, 6, 4, 5 ]))
    # print(merge_sort([2,2,3,8,1,-8,2,3,1,-8]))