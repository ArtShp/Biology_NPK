from random import randint

x = open('C:/Users/Admin/PycharmProjects/Biology_NPK/input/input.txt', 'w+')
arr = 'ARNDCQEGHILKMFPSTWYVBZX'

amount = 13
length = 300

for i in range(amount):
    s = ''
    for k in range(length):
        s += arr[randint(0, len(arr)-1)]
    x.write(s)
    if i+1 != amount:
        x.write('\n')

x.close()
