from config import *


# TODO -> Придумать нормальное название + описание + нормальный вывод
# TODO -> Добавить логирование ошибок(может не надо)
class CustomException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('Error occurred!')
        if self.message:
            return f'CustomException, {self.message}'
        else:
            return f'CustomException has been raised'
