from exceptions import *
from functions import *


s1 = 'ABЦ'*(10**2)
s2 = 'FEC'*(10**2)

print(len(s1), len(s2))

res = sequence_global_alignment(s1, s2, mode=1)
print(res)
