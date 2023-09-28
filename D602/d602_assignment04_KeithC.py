import numpy as np

#%% Q1
# Create a class called BankAccount that has four attributes: bankname, firstname, lastname, and balance.
# The default balance should be set to 0.
# In addition, create ...
    # ● A method called deposit() that allows the user to make deposits into their balance.
    # ● A method called withdrawal() that allows the user to withdraw from their balance.
    # ● Withdrawal may not exceed the available balance. Hint: consider a conditional argument in your withdrawal() method.
    # ● Use the __str__() method in order to display the bank name, owner name, and current balance.
    # ● Make a series of deposits and withdrawals to test your class.

class BankAccount:

    def __init__(self, bankname, firstname, lastname, balance = 0):
        self.bankname, self.balance = bankname, balance
        self.firstname, self.lastname = firstname, lastname

    def __str__(self):
        return str(
            f'This account is with {self.bankname} bank and owned by {self.firstname} {self.lastname}. '
            f'The current account balance is ${self.balance:.2f}.'
        )

    def deposit(self, amount):
        self.balance = self.balance + amount
        print(f'Successfully deposited ${amount:.2f}. Updated balance is ${self.balance:.2f}.')

    def withdrawal(self, amount):
        if amount > self.balance:
            print(f'Withdrawal amount (${amount:.2f}) exceeds account balance. Withdrawal cancelled.')
        else:
            self.balance = self.balance - amount
            print(f'Successfully withdrew ${amount:.2f}. Updated balance is ${self.balance:.2f}.')

myAccnt = BankAccount('Chase', 'John', 'Smith', 1000)

print(myAccnt)

myAccnt.deposit(100)
myAccnt.withdrawal(200)
myAccnt.deposit(1000)
myAccnt.withdrawal(2000)

print(myAccnt)

#%% Q2
# Create a class Box that has attributes length and width that takes values for length and width upon construction
# (instantiation via the constructor).
# In addition, create…
    # A method called render() that prints out to the screen a box made with asterisks of length and width dimensions
    # A method called invert() that switches length and width with each other
    # Methods get_area() and get_perimeter() that return appropriate geometric calculations
    # A method called double() that doubles the size of the box. Hint: Pay attention to return value here.
    # Implement __eq__ so that two boxes can be compared using ==. Two boxes are equal if their respective lengths
    # and widths are identical.
    # A method print_dim() that prints to screen the length and width details of the box
    # A method get_dim() that returns a tuple containing the length and width of the box
    # A method combine() that takes another box as an argument and increases the length and width by the dimensions
    # of the box passed in
    # A method get_hypot() that finds the length of the diagonal that cuts through the middle
    # Instantiate 3 boxes of dimensions 5,10 , 3,4 and 5,10 and assign to variables box1, box2 and box3 respectively
    # Print dimension info for each using print_dim()
    # Evaluate if box1 == box2, and also evaluate if box1 == box3, print True or False to the screen accordingly
    # Combine box3 into box1 (i.e. box1.combine())
    # Double the size of box2
    # Combine box2 into box1

class Box:

    def __init__(self, length, width):
        self.length, self.width = length, width

    def __str__(self):
        return str(f'Box of length {self.length} and width {self.width}.')

    def __eq__(self, other):
        return self.length == other.length and self.width == other.width

    def render(self):
        top_bot = str('*' * self.width)
        body = str('*' + ' ' * (self.width - 2) + '*')
        rendering = str(
            top_bot + '\n' +
            (body + '\n') * (self.length - 2) +
            top_bot
        )
        return rendering

    def print_dim(self):
        print(f'Length: {self.length} / Width: {self.width}')

    def get_dim(self):
        return (self.length, self.width)

    def get_perimeter(self):
        return self.length * 2 + self.width * 2

    def get_area(self):
        return self.length * self.width

    def get_hypot(self):
        return np.sqrt(self.length ** 2 + self.width ** 2)

    def invert(self):
        self.length, self.width = self.width, self.length

    def double(self):
        self.length, self.width = self.length * 2, self.width * 2

    def combine(self, other_box):
        self.length += other_box.length
        self.width += other_box.width

box1 = Box(5,10)
box2 = Box(3,4)
box3 = Box(5,10)

print('Box dimensions (1, 2, 3)')
box1.print_dim()
box2.print_dim()
box3.print_dim()

print(
    '\nBox equality\n' +
    f'Box1 versus Box2: {box1 == box2}\n'
    f'Box1 versus Box3: {box1 == box3}\n'
)

print(
    f'Box1 Initial: {box1.length} x {box1.width}\n' +
    box1.render() + '\n' +
    f'Perimeter: {box1.get_perimeter()}\n' +
    f'Area: {box1.get_area()}\n' +
    f'Hypotenuse: {box1.get_hypot():.4f}\n'
)

box1.combine(box3)
box2.double()
box1.combine(box2)

print(
    f'Box1 after combining with Box3 and doubled Box2: {box1.length} x {box1.width}\n' +
    box1.render() + '\n' +
    f'Perimeter: {box1.get_perimeter()}\n' +
    f'Area: {box1.get_area()}\n' +
    f'Hypotenuse: {box1.get_hypot():.4f}\n'
)

box1.invert()

print(
    f'Box1 after inversion: {box1.length} x {box1.width}\n' +
    box1.render() + '\n' +
    f'Perimeter: {box1.get_perimeter()}\n' +
    f'Area: {box1.get_area()}\n' +
    f'Hypotenuse: {box1.get_hypot():.4f}\n'
)
