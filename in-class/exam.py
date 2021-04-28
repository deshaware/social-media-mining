# # def main():
# #     try:
# #         total = int(input("Enter total cost of items? "))
# #         num_items = int(input("Number of items "))
# #         average = total / num_items

# #     except ZeroDivisionError:
# #         print('ERROR: cannot have 0 items')

# #     except ValueError:
# #         print('ERROR: number of items cannot be negative')

 

# # # if __name__ == '__main__':

# # #     main()


# # import random

# # # number = random(range(1, 50))
# # print(x/5)



# def main():
#     inp = int(input("Please enter a temperature: "))
#     while inp != 0:
#         if inp > 50 and inp < 104:
#             print("It is just right.")
#         elif inp >= 104:
#             print("It is hot.")
#         elif inp <= 50:
#             print("It is cold.")
#         inp = int(input("Please enter a temperature: "))
#     print("Good bye!")

# if __name__ == '__main__':
#     main()
    

from collections import Counter
c = Counter('011886227629412') 
print(c)
b = c # this statement is incomplete. Complete it.
print(len(b))    