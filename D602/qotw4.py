import numpy as np

#%% 1. Write a function to calculate the area and perimeter of a rectangle.

def rectangle(length, width):
    area = length * width
    perimeter = 2*length + 2*width
    return area, perimeter

area_a, perim_a = rectangle(3,5)
print(
    f'Area: {area_a:.3f}\n'
    f'Perimeter: {perim_a:.3f}\n'
)

area_b, perim_b = rectangle(6.7,2.45)
print(
    f'Area: {area_b:.3f}\n'
    f'Perimeter: {perim_b:.3f}\n'
)


#%% 2. Write a function to check if a number is even or not.  The function should indicate to the user even or odd.

def even_or_odd(input_):
    if type(input_) != int:
        print('Please provide an integer input.')
    elif input_ % 2 == 0:
        print('The number is even.')
    else:
        print('The number is odd.')

even_or_odd(1024)
even_or_odd(26)

even_or_odd(1027)
even_or_odd(9)

even_or_odd(9.25)
even_or_odd('Error.')

#%% 3. Write a Python function that accepts a string and calculate the number of upper case letters and lower case letters.
# Sample string: “CUNY sps”
# Number of upper case characters: 4
# Number of lower case characters: 3

def count_cases(input_string):
    upper = len([x for x in input_string if x.isupper()])
    lower = len([x for x in input_string if x.islower()])
    return upper, lower

upper, lower = count_cases('all lower')
print(
    f'Nb. of upper case letters: {upper}\n'
    f'Nb. of lower case letters: {lower}\n'
)

upper, lower = count_cases('ALL UPPER')
print(
    f'Nb. of upper case letters: {upper}\n'
    f'Nb. of lower case letters: {lower}\n'
)

upper, lower = count_cases('mIx iT uP')
print(
    f'Nb. of upper case letters: {upper}\n'
    f'Nb. of lower case letters: {lower}\n'
)

#%% 4. Write a Python function to sum all the numbers in a list

def sum_list(input_list):
    cleaned_list = [x for x in input_list if type(x) == int or type(x) == float]
    return sum(cleaned_list)

print(f'All integers: {sum_list([1,2,3])}')

print(f'All integers and floats: {sum_list([1,2,3,4.5])}')

print(f'Mixed bag: {sum_list([1,"two","three",4.5])}')

#%% 5. Create a function that shows an example of global vs local variables.

num1 = 1
num2 = 2
def add(x, y):
    z = x + y
    print('global symbol table:', globals())
    print('local symbol table:', locals())
    return z

add(num1,num2)

"""
If we run this as a standalone script, we will see only num1 and num2 in the globals() list, but the locals() list will include x, y and z, as they are part of the local environment of the add() function.
"""

#%% 6. Write a Python program to create a function that takes one argument, and that argument will be multiplied with an unknown given number.

def random_multiplying(input_number):
    return input_number * np.random.randint(0,100)

print(random_multiplying(5))
print(random_multiplying(2))
print(random_multiplying(7.5))