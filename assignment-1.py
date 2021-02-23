#Author: Swapnil Ghanshyam Deshaware
#: Social Media and Data Mining Assignment 1

#Domino's Pizza Counter
#Start with welcome, option to choose categories
#Categories - Pizza,Sides(Bread), Soda
#Payment - Billing and tip
#Discount - Enter today's day in CAPs to get 15%

#Problem is cart object is not updated even when the pizza added

class Cart():

    def __init__(self):
        '''
        Initializing the cart at the begining
        '''
        self.items = []
        self.amount = []
        self.count = 0
        self.bill = 0.0
    
    def add_item(self, item, bill):
        '''
        Adding new items to the cart, maintaining the value 
        '''
        self.items.append(item)
        self.amount.append(bill)
        self.bill += float(bill)
    
    def get_bill(self):
        # print(self)
        return self.bill
    
    def view_bill(self):
        '''
        A total bill can be viewed, total bill, tax etc and
        for decision making such as add/remove from the cart
        '''
        if self.count > 0:
            print("=====================Invoice========================")
            for i in range(self.count):
                print(f"{int(i+1)}. {self.items[i]}           \t${round(float(self.amount[i]),2)}\n".title())
            print("=====================Total==========================")
            print(f"Total Bill Before Tax:\t\t\t${round(float(self.bill),2)}\n")
            print(f"Total Tax            :\t\t\t${round(float(self.bill * 0.12),2)}\n")
            print(f"Total Bill           :\t\t\t${round(float(self.bill * 1.12),2)}\n")
        else:
            print("Your cart is empty\n")

    def remove_item(self):
        '''
        Listing all the items in the cart to remove at a position
        '''
        try:
            if(self.count > 0):
                print("-------------Cart-----------------\n")
                for i,x in enumerate(self.items):
                    print(f"{int(i+1)}\t{x}".title())
                rem = int(input("\nWhich item to remove:\n"))
                del self.items[(rem - 1)]
                self.bill -= self.amount[rem - 1]
                del self.amount[rem - 1]
                self.count -= 1
                print("\n 1 Item removed successfully")
            else:
                raise ValueError
        except ValueError:
            print("Invalid Option")
        except BaseException() as e:
            print(e)

    
    def __str__(self):
        return super().__str__()


class Food(Cart):

    def __init__(self):
        super().__init__()
        self.size = { 'regular': 3.99, 'medium': 4.99, 'large': 6.99 }
        self.pizza = { 'mushroom': 3.99, 'chicken': 4.99, 'spinach': 3.49, 'delux':5.99, 'veggie':3.99 }
        self.bread = { 'bacon':2.49, 'cheese':3.99, 'spinach':3, 'parmesan':3.49 }
        self.drink = { 'pepsi':2.99, 'coke':2.49, 'lemonade':3.39 }
        self.size_list = list(self.size.keys())
        self.pizza_list = list(self.pizza.keys())
        self.bread_list = list(self.bread.keys())
        self.drink_list = list(self.drink.keys())
    
    def getSize(self, type):
        return int(input(f"\nPlease select the following size for {type},\n1.Regular\n2.Medium\n3.Large\n"))

    def makePizza(self):
        '''
        This method is used to add pizza to the cart
        '''
        try:
            size = self.getSize('pizza')
            pizza_type = int(input("\nPlease select the following pizza type,\n1.Cheeseburger\n2.Chicken\n3.Spinach\n4.Delux\n"))
            if size < 1 or size > 3 or pizza_type < 1 or pizza_type > 4:
                raise ValueError("Invalid option")
            else:
                self.add_item(self.size_list[size - 1] + ' ' + self.pizza_list[pizza_type - 1] + ' pizza', float(self.size[self.size_list[size - 1]] + self.pizza[self.pizza_list[pizza_type  - 1]]))
                self.count += 1
                print("\n1 Pizza Added to the cart successfully\n")
        except ValueError as e:
            print(e)
        

    def makeBread(self):
        '''
        This method is used to add breads to cart
        '''
        try:
            size = self.getSize('bread')
            bread_type = int(input("\nPlease select the following bread type,\n1.Becon\n2.Cheese\n3.Spinach\n4.Parmesan\n"))
            if size < 1 or size > 3 or bread_type < 1 or bread_type > 4:
                raise ValueError("invalid option")
            else:
                self.add_item(self.size_list[size - 1] + ' ' + self.bread_list[bread_type - 1] + ' bread', float(self.size[self.size_list[size - 1]] + self.bread[self.bread_list[bread_type  - 1]]))
                self.count += 1
                print("\n1 Bread Added to the cart successfully\n")
        except ValueError as e:
            print(e)
    
    def addSoda(self):
        '''
        This method will add drinks to cart
        '''
        try:
            size = self.getSize('drink') 
            drink_type = int(input("\nPlease select the following drink type,\n1.Pepsi\n2.Coke\n3.Lemonade\n"))
            if size < 1 or size > 3 or drink_type < 1 or drink_type > 3:
                raise ValueError("invalid option")
            else:
                self.add_item(self.size_list[size - 1] + ' ' + self.drink_list[drink_type - 1] + ' soda', float(self.size[self.size_list[size - 1]] + self.drink[self.drink_list[drink_type  - 1]]))
                self.count += 1
                print("\n1 Drink Added to the cart successfully\n")
        except ValueError as e:
            print(e)

    def __str__(self):
        # return super().__str__()
        sb = ""
        for i in self.pizza.keys():
            print(i)

class Payment(Cart):
    def __init__(self):
        self.coupons = {'JAN': 0.2, 'FEB': 0.25}
        self.tax = 0.49
    
    def makePayment(self,food):
        print("Processing Your Payment")
        '''
        Check if the discount applicable
        '''
        discount = input("\nDo you have an discount coupon, Yes or No:\n")
        if discount == 'Yes':
            print(f"Your bill with discount is ${round(food.bill * 0.9, 2)}")
            print(f"Your total bill is ${round(food.bill * 1.02, 2)}")
        else:
            print(f"Your current bill is ${round(food.bill * 1.12, 2)}")
        print("payment is successful!")

def main():
    '''
    This method is an entry to Domino's Pizza Service
    '''
    try:
        print("Welcome to Domino's Pizza!'\nWhat are you having today?\n")
        options = input("\t1.Pizza\n\t2.Breads\n\t3.Soda\n\t4.View Cart\n\t5.Remove Item\n\t6.Pay Bill\n\t7.Quit\n")
        food = Food()
        while options != '7':
            if options == '1':
                #get your pizza ready
                food.makePizza()
            elif options == '2':
                #Make Breads
                food.makeBread()
            elif options == '3':
                #Make a drink
                food.addSoda()
            elif options == '4':
                #View Cart
                food.view_bill()
            elif options == '5':
                #Remove An Item
                food.remove_item()
            elif options == '6':
                #Exit
                break
            else:
                print("Please try with digit 1 - 5")
            options = input("\nDo you want to add/remove anything else\n\t1.Pizza\n\t2.Breads\n\t3.Soda\n\t4.View Cart\n\t5.Remove Item\n\t6.Pay Bill\n\t7.Quit\n")
            
        if options == '7' and food.count < 1:
            return print("\nThank you for stopping by!")
        else:
            print("Payment Processing")
            pay = Payment()
            pay.makePayment(food)
            print("\n Here's your invoice")
            food.view_bill()
            print("\nYour pizza will be delivered shortly, Thank you for stopping by\n")
    # except ValueError:
    except ValueError:
        print("Invalid Option")
    

if __name__ == '__main__':
    main()