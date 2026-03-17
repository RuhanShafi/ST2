#Week_3_ROL_Tutorial_Activity_1
import random as r

# These will need to be demonstrated in the ROL Lab environment and uploaded to GitHub after tutor signoff.

# LISTS
# Lists are one of the fundamental data structures available to us in standard Python.
# Lists are also referred to as sequences data structure in programming domains
# Lists are an ordered collection of data represented in Python by [] and elements separated
# with commas such as [1, 2, 3].
# Lists *can* contain elements of different types, but for most use cases they will end up 
# containing a single type.

# How do we create a list?
my_list = [] # Creates an empty list.
my_list  = [1, 2, 3]
my_list  = ['a', 2, []]
my_list 

# We'll stick with a list of integers for now, though.
my_list  = [1, 2, 3, 4, 5]

# Basic sequence functionality
# Indexing
# Sequence data structures are indexed, meaning that elements have a ordering to them 
# and can be accessed by their index (starting with 0).

# Indices always start with 0, not 1 (this is called 'zero-based indexing' and is common to many programming languages)
my_list [0]
my_list [4]

# Negative indices will start from the opposite end of the list. Note that negative indices are indexed starting at -1, not 0.
my_list [-1]
my_list [-5]


# Indices can be used to update an element in a particular position.
# Lists, unlike some other data structures like tuples, are mutable, meaning
# their contents can be changed dynamically without creating a whole new copy of the structure.
my_list [0] = 10

del my_list [0]


# Slicing
# Slicing allows us to grab sub-sections of the sequence based on indices.
# All slice operations return a new list containing requested elements (shallow copy)

# Slicing syntax
# sequence[start:stop:step]

# Stop index is exclusive!

# Reading from a slice
my_list[0:2] # Gives us elements at indices 0, 1 (2 is exclusive)
my_list[-2:]
my_list [0:] # Both of these print the whole sequence
my_list [:] # There is an 'implicit' start and stop index, namely the first and last elements of the sequence.

# You can also specify a step for the slice
my_list [0:5:2] # Step of 2

# Assigning to a slice
# You can also use slices to insert and delete elements.
my_list [2:5] = [30, 40, 50]

# The addition does not need to be the same length as the range
my_list [2:5] = [30, 40, 50, 60, 70, 80]

# Deleting with a slice
my_list [2:5] = []


# Concatenation
# Lists can be concatenated with the + operator
new_list = [1, 2, 3]

# Lists can also be nested inside one another!
nested_list = [[1, 2, 3], [1, 2, 3]]



# LIST METHODS
# Aside from built in sequence syntax, lists have a set of methods that can be called as well.

# One of the most common list methods is .append(). This allows us to add an item to the end of the list.
my_list  = [1, 2, 3]
my_list.append(4)

# You can append the contents of an entire other sequence with .extend()
my_list.extend([5, 6])

# If you need to insert an element at a particular index, you can use the .insert() function.
# It takes an index and the item to be inserted.
my_list.insert(1, 100)


# There are also methods for removing and deleting elements.
my_list.remove(100) # Removes first occurence of a value.

my_list.pop(4) # Remove item at index
my_list.clear() # Reverts to empty list.


# Utility functions
# Lists also provide some utility functions that can be helpful in various scenarios.


my_list.extend([1, 1])
my_list.count(1) # Returns number of occurences of a particular item

# Some functions dealing with list ordering.
my_list.sort()
my_list.reverse()

# A helpful utility function that can be applied to all sequences is the built-in len() function,
# which returns the length of the sequence.
len(my_list)

# Note that some of these methods' functionality can be replicated using base sequence syntax that 
# we learned previously, but using the methods may be a preferable option for making code more readable.

# Don't worry about memorizing all these functions . 
# This is more to give you an idea of what's possible with lists. 
# As always, you will become more comfortable with using these structures given
# time and practice.


# Iterating a sequence and member checking
# Iterating through the elements in a data structure is a very common programming task.
# Python provides some convenient syntax for iterating through the contents of a sequence: the for loop

# For loops in Python appear more like 'for-each' loops in other languages.
for n in my_list:
    print(n)

# 'in' keyword
# Another useful Python construct that applies to most data structures is the ability to check
# membership.
100 in my_list 
50 in my_list 



# LIST COMPREHENSIONS

# Python provides a fairly unique syntax for filtering lists and applying operations to list elements.
my_list  = [1, 2, 3, 4, 5]
my_list  = [n for n in my_list if n > 3] # Filtering

my_list  = [n**2 for n in my_list] # Applying operation

# Equivalency to for-loops
# List comprehensions are not strictly necessary, but can provide a more succint, readable syntax 
# alternative to for loops with nested conditionals.
new_list = []
for n in my_list:
    if n > 3: new_list.append(n)


# STRINGS
# While we don't usually think of strings as data structures, it is important to note that in Python they are
# also a type of sequence. Practically, this means that many of the same syntax for manipulating and accessing lists
# can be used with strings such as indexing, slicing, concatenation, etc.
string = 'This is a string!'

string[0]
string[0:5]

# One key difference, though, is that strings are immutable. So you cannot append or update indices.

# Strings also have their own set of useful methods, including some familiar ones from the list data structure.
string.index('is')
string.replace('a', 'the')
string.count('i')



# DICTIONARIES
# Dictionaries are another fundamental data structure in Python. Unlike every other
# structure we're covering in this course, dictionaries are not sequences. They are
# a unique Python type, also called a Mapping Type.

# A dictionary is a set of key: value pairs.
# Keys must be unique.

# You can declare an empty dictionary like so:
d = {}
# You can declare a dictionary with elements as well.
d = {'apple': 2, 'pear': 3}

d['apple']

d['blueberry'] = 1

d.keys()
d.values()

# Safer way to get an item
d.get('apple', 'default')
d.get('grape', 'default') # Doesn't crash, unlike d['grape']

d.pop('blueberry') # Removes an element by key

# Dictionaries, like Maps in other languages, are a backbone of programming in Python.
# Almost every program of any complexity will make use of them.


# Looping through a dictionary with .items()
for k, v in d.items():
    print(k, v)


# Dictionary comprehensions
# Used similarly to list comprehensions, can create new dictionaries
# filtering or applying operations.
{x: x**3 for x in (1, 2, 3)}

{k.upper(): v*2 for k, v in d.items()}



# Now we take a look at two
# more varieties of sequence that can be useful.

# TUPLES
# Tuples are a data structure similar to lists, but with some key differences.
t = (1, 2, 3)

# Tuples are immutable.
# You cannot change the contents of a tuple once created, you must make a new tuple.
# This property is helpful for ensuring data integrity.

# Because tuples are immutable, they are hashable, and so can be used 
# as keys in dictionaries, whereas lists cannot.
td = {(1,2): 1, (2,3): 2}

# You will often encounter tuples when functions need to return complex data
# in a structured way. They are particularly amenable to 'unpacking'.
# For instance, dict.items() returns a list of tuples.
def tuple_example():
    return ('apple', 'fruit', 2.99)

fruit, kind, price = tuple_example() # Unpacking

# Tuples can also be 'packed' in a similar manner
t = fruit, kind, price

#  Sequence unpacking requires that there are as many
#  variables on the left side of the equals sign as there are elements in the sequence.



# SETS
# Finally, we have sets. Sets are an unordered collection with no duplicate elements.
# Some uses for sets include eliminating duplicates, and membership testing.

# In fact, we've already seen a data structure that has set-like properties.
# In dictionaries, recall that the set of keys must contain only unique elements.
# This essentially makes dictionary keysets, well, sets!
a = set()
a = {1, 2, 3, 4}
a.add(4) # This will not do anything, since 4 is already a member of the set.

# There are also some interesting operations that sets allow.
b = {4, 5, 6, 7}
a | b
a & b


# CHALLENGE 
# Challenge: Write a function that takes a list and outputs a 
# list of tuples that contain each unique element of the list
# alongside the number of times that element appears in the list.

# For example, if the input is [1, 2, 2, 3, 4, 4, 5, 1]
# The output would be [(1, 2), (2, 2), (3, 1), (4, 2), (5, 1)]

def list_count(l):
    output = []
    seen = set()

    for n in l:
        if n not in seen:
            seen.add(n)
            n_count = l.count(n)
            output.append((n, n_count))

    return output

l = [1, 2, 2, 3, 4, 4, 5, 1]

