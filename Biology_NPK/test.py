from exceptions import *

try:
    raise CustomException
except CustomException:
    print(1)
