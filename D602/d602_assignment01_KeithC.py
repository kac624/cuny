# Q1 Fix all the syntax and logical errors in the given source code
# add comments to explain your reasoning

# This program gets three test scores and displays their average.  It congratulates the user if the 
# average is a high score. The high score variable holds the value that is considered a high score.

#%%
HIGH_SCORE = 95
 
# Get the test scores.
test1 = input('Enter the score for test 1: ')
test2 = input('Enter the score for test 2: ')

'''
    Another variable is required to capture
    results for test #3. The `average` variable
    looks for the vlariabe `test3`, so I've named
    the missing variable accordingly.
'''
test3 = input('Enter the score for test 3: ')

# Calculate the average test score.

'''
    The `input()` function returns strings,
    so we must explicitly convert our test
    results variables to a numerical data
    type. I chose floats to avoid rounding.
'''
test1 = float(test1)
test2 = float(test2)
test3 = float(test3)

'''
    The average function below lacked parentheses
    around the test scores to be summed. Because of
    order of operations, the code was read as:
    test1 + test2 + (test3 / 3). I added parenthesis
    to correctly calculate the average.
'''
average = (test1 + test2 + test3) / 3

# Print the average.
print(f'The average score is {average:.2f}')

# If the average is a high score,
# congratulate the user.

'''
    The high_score variable was never defined.
    I've set the high score as an arbitrary 90.
'''
high_score = 90

if average >= high_score:
    print('Congratulations!')
    
    '''
        The second print statement was not properly indented.
        As a result, the program printed 'That is a great
        average!' every time, regardless of how high or low
        the scores were. By indenting this print call, the 
        program only prints this final statement when the
        high_score is exceeded.
    '''
    print('That is a great average!\n')
#%%

#Q2
#The area of a rectangle is the rectangle’s length times its width. Write a program that asks for the 
#length and width of two rectangles and prints to the user the area of both rectangles.
#%%
length1 = float(input('Enter the LENGTH of the first rectangle: '))
width1 = float(input('Enter the WIDTH of the first rectangle: '))

length2 = float(input('Enter the LENGTH of the second rectangle: '))
width2 = float(input('Enter the WIDTH of the second rectangle: '))

print(
  f'The first rectangle has an area of {round(length1 * width1,3)} square units.',
  f'\nThe second rectangle has an area of {round(length2 * width2,3)} square units.',
  '\n'
)
#%%

#Q3 
#Ask a user to enter their first name and their age and assign it to the variables name and age. 
#The variable name should be a string and the variable age should be an int.  

# Using the variables name and age, print a message to the user stating something along the lines of:
# "Happy birthday, name!  You are age years old today!"

#%%
name = input('Enter your first name: ')
age = int(input('Enter your age in years: '))

print(f'Happy birthday, {name}!  You are {age} years old today!')
#%%


