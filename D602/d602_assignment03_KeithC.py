import numpy as np

#%%

# Q1: Write a program that prompts the user for a meal: breakfast, lunch, or dinner. Then using if statements and else
# statements print the user a message recommending a meal. For example, if the meal was breakfast, you could say
# something like, “How about some bacon and eggs?”
# The user may enter something else in, but you only have to respond to breakfast, lunch, or dinner.

recommendations = {
    1:'Try starting the day with eggs and toast.',
    2:'Oatmeal is great for breakfast.',
    3:"You can't go wrong with a PB&J.",
    4:'I recommend a BLT!',
    5:'Perhaps a salad?',
    6:'Nothing like a Chicken Alfredo to really fill ya up.',
    7:'Screw it! Tonight is a steak night.'
}

def make_recommendation(meal):
    if meal == 'breakfast':
        rng = np.random.randint(1,3)
        print(recommendations[rng])
    elif meal == 'lunch':
        rng = np.random.randint(3, 6)
        print(recommendations[rng])
    elif meal == 'dinner':
        rng = np.random.randint(5, 8)
        print(recommendations[rng])
    else:
        print(
            'Entry not recognized; please try again.',
            'You should enter one of the following: breakfast, lunch or dinner.'
        )

def q1_main():
    meal = input('Choose a meal (breakfast, lunch or dinner): ')
    make_recommendation(meal)

q1_main()

#%%

# Q2: The mailroom has asked you to design a simple payroll program that calculates a student employee’s gross pay,
# including any overtime wages. If any employee works over 20 hours in a week, the mailroom pays them 1.5 times their
# regular hourly pay rate for all hours over 20.
# You should take in the user’s input for the number of hours worked, and their rate of pay.

class Employee:

    def __init__(self, name = '', rate = 0):
        self.name = name
        self.rate = rate

    def calculate_pay(self, hours_worked):
        if hours_worked <= 20:
            pay = hours_worked * self.rate
        else:
            base_pay = hours_worked * self.rate
            overtime = (hours_worked - 20) * self.rate * 0.5
            pay = base_pay + overtime

        return pay

pay_rates = {
    'John': 20,
    'Jill': 23,
    'Jack': 22,
    'Omar': 21,
    'Yao': 25,
    'Burt': 19,
    'Marta': 26,
}

def q2_main():
    while True:
        name = input('Please enter your name: ')
        emp = Employee(name)
        try:
            emp.rate = pay_rates[name]
        except:
            print('Name not found. Please try again.')
            pass
        else:
            break

    hours_worked = float(input('Please enter the number of hours worked: '))
    pay = emp.calculate_pay(hours_worked)

    print(f'Hello, {emp.name}. With a rate of ${emp.rate:.2f} '
          f'per hour, your pay for this week is ${pay:.2f}.')

q2_main()

#%%

# Q3: Write a function named times_ten. The function should accept an argument and display the product of its argument
# multiplied times 10.

def times_ten(input_):
    return input_ * 10

print(
    times_ten(10),'\n',
    times_ten(3),'\n',
    times_ten(115),'\n'
)

#%%

# Q4: Find the errors, debug the program, and then execute to show the output.
#
# def main()
#       Calories1 = input( "How many calories are in the first food?")
#       Calories2 = input( "How many calories are in the first food?")
#       showCalories(calories1, calories2)
#
# def showCalories()
#    print(“The total calories you ate today”, format(calories1 + calories2,.2f))

def q4_main():
      calories1 = float(input( "How many calories are in the first food?"))
      calories2 = float(input( "How many calories are in the second food?"))
      showCalories(calories1, calories2)

def showCalories(calories1, calories2):
   print("The total calories you ate today: {0:.2f}".format(calories1 + calories2))

q4_main()

#%%

# Q5: Write a program that uses any loop (while or for) that calculates the total of the following series of numbers:
#          1/30 + 2/29 + 3/28 ............. + 30/1

numerator = 1
denominator = 30
results = []

while denominator > 0:
    result = numerator / denominator
    results.append(result)
    numerator += 1
    denominator -= 1

print(f'Result: {sum(results):.3f}')

#%%

# Q6: Write a function that computes the area of a triangle given its base and height.
# The formula for an area of a triangle is: AREA = 1/2 * BASE * HEIGHT
#
# For example, if the base was 5 and the height was 4, the area would be 10.
# triangle_area(5, 4)   # should print 10

def triangle_area(base, height):
    return base * height * 0.5

print(
    triangle_area(5,4),'\n',
    triangle_area(6.5,3),'\n',
    triangle_area(50.99,201.647)
)