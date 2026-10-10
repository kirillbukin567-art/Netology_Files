# Глобальная переменная для хранения votes_count
votes_count_global = None

def check_votes_count(votes_count):
    """Функция для проверки подсчёта голосов (не изменяйте её)"""
    global votes_count_global
    votes_count_global = votes_count
    return votes_count

# Впишите ваше решение в функцию vote
def vote(votes):
    # используется для проверки корректности словаря
    # не убирайте эти две строки
    global votes_count_global
    votes_count_global = None

    # 1) создайте словарь для подсчёта голосов
    votes_count = {}
    for candidate in votes:
        if candidate in votes_count:
            votes_count[candidate] += 1
        else:
            votes_count[candidate] = 1

    # проверка словаря, не убирайте строку ниже
    votes_count_global = check_votes_count(votes_count)

    # 3) найдите максимальное количество голосов
    max_votes = max(votes_count.values())

    # 4) найдите всех кандидатов с максимальным количеством голосов
    winners = []
    for candidate, count in votes_count.items():
        if count == max_votes:
            winners.append(candidate)

    # 5) верните результат в зависимости от количества победителей
    if len(winners) == 1:
        return winners[0]
    else:
        return "Нужен второй тур выборов"


if __name__ == '__main__':
    citizens_votes = [
        [3, 2, 3, 2, 1, 1, 1, 3, 1, 1],
        [1, 1, 2, 1, 2, 1, 3, 3, 3, 3, 2, 1, 2, 1, 1],
        [1, 2, 2, 3, 2, 1, 1, 3, 2, 3, 2, 2, 3, 3, 1, 2, 1, 3, 3, 1],
        [2, 2, 1, 3, 3, 2, 3, 1, 1, 2, 1, 2, 2, 2, 3],
        [3, 3, 2, 2, 1, 3, 1, 2, 3, 1, 2, 2, 1, 3, 3],
    ]

    for i, votes_list in enumerate(citizens_votes):
        print(f"Результат {i+1}: {vote(votes_list)}")