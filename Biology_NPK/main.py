from config import *
from exceptions import *
from functions import *

score_mode = 1

s1 = 'CCAAGGCT'
s2 = 'CCAGAGAC'

res1 = sequence_global_alignment(s1, s2, score_mode)
res2 = sequence_local_alignment(s1, s2, score_mode)
print(res1, end='\n\n')
print(res2)
"""
f = open('../resources/blosum62.txt', 'r+')
s = f.read()
s = s.strip().split('\n')

header = s.pop(0)
columns = header.split()
matrix = {}

for row in s:
  entries = row.split()
  row_name = entries.pop(0)
  matrix[row_name] = {}

  if len(entries) != len(columns):
    raise Exception('Improper entry number in row')
  for column_name in columns:
    matrix[row_name][column_name] = entries.pop(0)


print(matrix)
a = {default: '3'}
print(a[5])
"""


