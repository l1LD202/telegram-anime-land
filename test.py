

from random import randrange
print(randrange(1, 100))

# 2)
num_list = input('Enters a sequence of numbers like: 1 48 23\n').split(' ')
result = 0
for num in num_list:
    result += int(num)

print(result/len(num_list))

# 3)
set_a = input('Enter first squence of numbers like: 1 25 59\n').split(" ")
set_b = input('\nEnter second squence of numbers like: 1 25 59\n').split(" ")

print(set(set_a) - set(set_b))