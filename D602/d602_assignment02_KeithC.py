# %%
# Q1. What will the following code display?

numbers = [1, 2, 3, 4, 5]
print(numbers[1:-5])

'''
It displays nothing because of the indexing. First, indices in Python
begin from 0, so the first index of 1 actually excludes the first item
in the list. Second, adding a negative to an index indicates that counting
should begin from the end of the list. So, a -5 indicates the fifth item
from the end of the list (i.e. the first item). So, in total, the print 
command slices the list starting with the second item and ending with the 
first. In other words, it calls nothing.
'''

# Can you debug and fix the output? The code should return the entire list

'''
To display the entire list. You can slice from the first item (i.e. [0])
to the last (i.e. [5], since the second index in a slice is exclusive). 
Alternatively, you could leave the second index blank, indicating the slice
should continue from the first index through the end of the list. Finally,
you could just skip the slice altogether and print the entire list, since
we want all elements.
'''

print('Corrected code 1:', numbers[0:5])

print('Corrected code 2:', numbers[0:])

print('Corrected code 3:', numbers)

# %%

# %%
# Q2. Design a program that asks the user to enter a store’s sales for each day of the
# week. The amounts should be stored in a list. Use a loop to calculate the total sales for
# the week and display the result.

days = ['Mon','Tues','Wednes','Thurs','Fri','Sat','Sun']
sales = []

for day in days:
    sales_daily = float(input(f'Enter the total sales (in dollars) for {day}day: '))
    sales.append(sales_daily)

cumulative_sales = 0

for sales_daily in sales:
    cumulative_sales += sales_daily

print(f'Total sales for the week were ${cumulative_sales:,.2f}')

# %%

# %%
# Q3. Create a list with at least 5 places you’d like to travel to. Make sure the list isn’t in
# alphabetical order
# ● Print your list in its original order.
# ● Use the sort() function to arrange your list in order and reprint your list.
# ● Use the sort(reverse=True) and reprint your list.

destinations = ['Hong Kong', 'Buenos Aeries', 'Tokyo', 'Cairo', 'Cape Town', 'Rio']

print('Original list:', destinations)

destinations.sort()

print('Sorted list:', destinations)

destinations.sort(reverse = True)

print('Reverse Sorted list:', destinations)

# %%

# %%
# Q4. Write a program that creates a dictionary containing course numbers and the room
# numbers of the rooms where the courses meet. The program should also create a
# dictionary containing course numbers and the names of the instructors that teach each
# course. After that, the program should let the user enter a course number, then it should
# display the course’s room number, instructor, and meeting time.

class_locations = {
    'D602':'Room 215',
    'D605':'Room 403',
    'D606':'Room 900',
    'D607':'Room 105'
}

class_instructors = {
    'D602':'Schettini',
    'D605':'Fulton',
    'D606':'Lui',
    'D607':'Catlin'
}

class_times = {
    'D602':'06:00pm',
    'D605':'07:00pm',
    'D606':'06:30pm',
    'D607':'05:45pm'
}

class_number = input('Enter the course number in "D###" format: ')

if class_number in class_locations.keys():
    print(
        f'\nDetails for {class_number}:\n\n'
        f'Class Location: {class_locations[class_number]}\n'
        f'Class Instructor: {class_instructors[class_number]}\n'
        f'Class Meeting Time: {class_times[class_number]}'
    )
else:
    print('Class not found.')

# %%

# %%
# Q5. Write a program that keeps names and email addresses in a dictionary as
# key-value pairs. The program should then demonstrate the four options:
# ● look up a person’s email address,
# ● add a new name and email address,
# ● change an existing email address, and
# ● delete an existing name and email address

import sys

emails = {
    'Keith':'keith.colella@gmail.com',
    'John':'john.doe@gmail.com',
    'Jane':'jane.doe@gmail.com',
    'Larry':'larry.johnson@gmail.com'
}

option = input(
    'Please choose from the following options.'
    '\n1. Look up email address.'
    '\n2. Add a new name and email.'
    '\n3. Change an existing email address.'
    '\n4. Delete an existing name and email.'
    '\nEnter the number corresponding to your choice: '
)

try:
    option = int(option)
except:
    print('Please enter your choice as a number.')
    sys.exit()


if option == 1:
    name = input('Please enter the name of the individual: ')
    try:
        email = emails[name]
        print(f'Email address for {name}: {email}')
    except:
        print('Name not found.')
elif option == 2:
    name = input('Please enter the name of the new individual: ')
    email = input('Please enter their email address: ')
    emails[name] = email
    print(f'Successfully added {name} and {email} to the database.\n',emails)
elif option == 3:
    name = input('Please enter the name of the individual whose email you wish to update: ')
    if name in emails.keys():
        email = input('Please enter the updated email: ')
        emails[name] = email
        print(f'The email for {name} was updated.\n',emails)
    else:
        print('Name not found.')
elif option == 4:
    name = input('Please enter the name of the individual you wish to delete: ')
    email = emails[name]
    removed = emails.pop(name, 'Name not found.')
    if removed == 'Name not found.':
        print(removed)
    else:
        print(f'Successfully removed {name} / {email}.\n',emails)
else:
    print('Option not found.')

# %%