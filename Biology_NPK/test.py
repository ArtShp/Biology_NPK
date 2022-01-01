from random import randint

x = open('C:/Users/user/Desktop/Biology_NPK/input/input_long.txt', 'w+')
arr = 'ARNDCQEGHILKMFPSTWYVBZX'

amount = 100
length = 300

for i in range(amount):
    s = ''
    for k in range(length):
        s += arr[randint(0, len(arr)-1)]
    x.write(s)
    if i+1 != amount:
        x.write('\n')

x.close()
