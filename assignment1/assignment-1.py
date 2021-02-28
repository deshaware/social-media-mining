"""
Social Media and Data Mining Assignment 1
Author: Swapnil Ghanshyam Deshaware
SUID: 253579042

#Domino's Pizza Counter
#Start with welcome, option to choose categories
#Categories - Pizza, Bread and Soda
#Payment - Billing and tax
#Discount - Depends on the month, default selected march for simplicity
"""

class Cart():
    '''
    Cart class to store 
    Items
    Amount
    Count of Items
    Total Bill
    '''

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
    
    def view_cart(self):
        '''
        View the current cart which will show the items inside the cart
        '''
        if self.count > 0:
            print("=====================My Cart========================")
            #Dictionary comprehension
            mycart = { (key+1): (item,round(float(self.amount[key]),2)) for (key,item) in enumerate(self.items)}
            for key,(item,amount) in mycart.items():
                print(f"{key}. {item}             \t${amount}".title())
        else:
            print("Your cart is empty\n")

    def view_bill(self, discount):
        '''
        A total bill can be viewed, total bill, tax etc and
        for decision making such as add/remove from the cart
        '''
        if self.count > 0:
            print("=====================Invoice========================")
            for i in range(self.count):
                print(f"{int(i+1)}. {self.items[i]}           \t${round(float(self.amount[i]),2)}\n".title())
            print("=====================Total==========================")
            print(f"Total Bill Before Tax:\t\t\t${round(float(self.bill),2)}")
            print(f"Total Tax            :\t\t\t${round(float(self.bill * 0.12),2)}\n")
            print(f"Total Bill           :\t\t\t${round(float(self.bill * 1.12),2)}\n")
            if discount:
                print(f"Total Discount       :\t\t\t${round((float(self.bill * 1.12) - float(self.bill * 1.02)),2)}")
                print(f"Bill After Discount  :\t\t\t${round(float(self.bill * 1.02),2)}\n")
        else:
            print("Your cart is empty\n")

    def remove_item(self):
        '''
        Listing all the items with the indexes
        So that items can be removed at that index
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
            print("Invalid Option, Cannot Remove Items from the empty cart")
        except BaseException():
            print("Invalid Option!")


class Payment(Cart):
    def __init__(self):
        self.coupons = {'JAN': 0.9, 'FEB': 0.88, 'MAR': 0.9}
    
    def makePayment(self,food):
        print("Processing Your Payment!")
        '''
        Method provides discount facility, which is prebuilt
        Yes and No option is asked to the user so that
        the bill and discound can be applied before taxes
        '''
        discount = input("\nDo you have an discount coupon, Yes or No:\n")
        if discount.upper() in ['YES', 'Y', 'Ye']:
            print(f"Your bill with discount before tax is ${round(food.bill * self.coupons['MAR'], 2)}\n") 
            food.view_bill(True)
        else:
            print(f"Your current bill is ${round(food.bill * 1.12, 2)}\n")
            food.view_bill(False)
        print("payment is successful!\n")

class Food(Cart):
    '''
     Main class holds valuable dictionaries with menu and the prices
     Inherited from the cart so that it has all the properties to 
     add and remove the data in the Cart class
    '''

    def __init__(self):
        super().__init__()
        self.size = { 'regular': 3.99, 'medium': 4.99, 'large': 7.99 }
        self.pizza = { 'mushroom': 3.99, 'chicken': 4.99, 'spinach': 3.49, 'delux':5.99, 'veggie':3.99 }
        self.bread = { 'bacon':2.49, 'cheese':3.99, 'spinach':3, 'parmesan':3.49 }
        self.drink = { 'pepsi':2.99, 'coke':2.49, 'lemonade':3.39 }
        self.size_list = list(self.size.keys())
        self.pizza_list = list(self.pizza.keys())
        self.bread_list = list(self.bread.keys())
        self.drink_list = list(self.drink.keys())
    
    def getSize(self, type):
        '''
        Returns the available size of breads, pizza and drinks
        '''
        return int(input(f"\nPlease select the following size for {type},\n1.Regular\n2.Medium\n3.Large\n"))

    def makePizza(self):
        '''
        It adds pizza to the cart
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
        except ValueError:
            print("Invalid Option!")
        
    def makeBread(self):
        '''
        It adds breads to cart
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
        except ValueError:
            print("Invalid Option")
    
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
        '''
        To Print The Menu
        '''
        sb = "Our Today's Menu is\n"
        #list comprehension
        pizza = [ "=> " +pizza.title()+" Pizza   \t\t$"+str(price) for pizza, price in self.pizza.items() ]
        bread = [ "=> " +bread.title()+" Bread   \t\t$"+str(float(price)) for bread, price in self.bread.items() ]
        soda = [ "=> " +drink.title()+" drink    \t\t$"+str(price) for drink, price in self.drink.items() ]
        sb += "\n\tPizza\n\t-----\n"
        for i in pizza:
            sb += i + "\n"
        sb += "\n\tBreads\n\t------\n"
        for i in bread:
            sb += i + "\n"
        sb += "\n\tDrinks\n\t------\n"
        for i in soda:
            sb += i + "\n"
        return sb

def main():
    '''
    This method is an entry to Domino's Pizza Service
    There are 1 - 8 options in order to generate order
    '''
    try:
        print("Welcome to Domino's Pizza!\nWhat are you having today?\n")
        options = input("\t1.Pizza\n\t2.Breads\n\t3.Soda\n\t4.View Cart\n\t5.Remove Item\n\t6.View Menu\n\t7.Pay Bill\n\t8.Quit\n")
        food = Food()
        while options != '8':
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
                food.view_cart()
            elif options == '5':
                #Remove An Item
                food.remove_item()
            elif options == '6':
                # view menu
                print(food)
            elif options == '7' and food.count < 1:
                #empty cart before billing case
                print("Cannot Process Payment!Your Cart is Empty\nAdd Delicious Pizza/Bread/Drink to your cart before you proceed")
            elif options == '7' and food.count > 0:
                #break
                break
            else:
                print("Invalid Option, Please try with digit 1 - 8")
            options = input("\nDo you want to add/remove items\n\t1.Pizza\n\t2.Breads\n\t3.Soda\n\t4.View Cart\n\t5.Remove Item\n\t6.View Menu\n\t7.Pay Bill\n\t8.Quit\n")
            
        if options == '8':
            return print("\nThank you for stopping by!")
        elif options == '7':
            pay = Payment()
            pay.makePayment(food)
            print("\nYour pizza will be delivered shortly, Thank you for stopping by!\n")
    # except ValueError:
    except ValueError:
        print("Invalid Option")
    

if __name__ == '__main__':
    '''
    Starting Point of execution, by calling the main method
    '''
    main()