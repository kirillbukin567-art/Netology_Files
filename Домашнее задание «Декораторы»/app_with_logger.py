"""Задание 3: логгер применён к приложению из д/з 2 (плоский генератор любой вложенности)."""
from logger_2 import logger


def flat_generator(list_of_list):
    for item in list_of_list:
        if isinstance(item, list):
            yield from flat_generator(item)
        else:
            yield item


@logger('flatten.log')
def flatten(list_of_list):
    # Логируем именно результат, поэтому возвращаем список, а не генератор
    return list(flat_generator(list_of_list))


if __name__ == '__main__':
    nested = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]
    print(flatten(nested))
    print('Запись в flatten.log:')
    with open('flatten.log', encoding='utf-8') as f:
        print(f.read())