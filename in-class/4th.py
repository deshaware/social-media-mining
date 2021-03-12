# Python3 program for the above approach 

# Function to find the duplicate 
# number using counting sort method 
def findDuplicate(arr, n): 

	# Initialize all the elements 
	# of the countArr to 0 
	countArr = [0] * (n + 1) 

	# Count the occurences of each 
	# element of the array 
	for i in range(n + 1): 
		countArr[arr[i]] += 1

	a = False

	# Find the element with more 
	# than one count 
	for i in range(1, n + 1): 
		if(countArr[i] > 1): 
			a = True
			print(i, end = " ") 

	# If unique elements are there 
	# print "-1" 
	if(not a): 
		print(-1) 

# Driver code 
if __name__ == '__main__': 

	# Given N 
	n = 6

	# Given array arr[] 
	arr = [ 1, 3, 44, 2, 2, 3 ] 

	# Function Call 
	findDuplicate(arr, n) 

# This code is contributed by Shivam Singh