"""Задача №1: unit-тесты на три задания из модуля «Основы Python» (pytest, с параметризацией)."""
import pytest

import voting
from courses import check_corr
from voting import vote
from worktime import count_worktime


# ---------- Задание: подсчёт рабочего времени ----------

@pytest.mark.parametrize(
    'todo_list, workday, expected',
    [
        # список из задания: 1 + 2 + 0.6 + 3 + 0.4 = 7 часов, на перерывы остаётся 1
        ([["Разобрать почту", 1], ["Обзвонить клиентов", 2], ["Запланировать дела на завтра", 0.6],
          ["Сделать презентацию", 3], ["Созвон с командой", 0.4]], 8, 1.0),
        # пустой список: весь рабочий день свободен
        ([], 8, 8.0),
        # задачи занимают весь день
        ([["Одна большая задача", 8]], 8, 0.0),
        # нестандартная длина рабочего дня
        ([["Задача", 1.5]], 6, 4.5),
        # дробные числа не должны давать погрешность в ответе
        ([["a", 0.1], ["b", 0.2]], 8, 7.7),
        # переработка: результат отрицательный
        ([["Срочная работа", 9]], 8, -1.0),
    ],
    ids=['пример из задания', 'пустой список', 'весь день занят', 'рабочий день 6 часов',
         'дробные значения', 'переработка'],
)
def test_count_worktime(todo_list, workday, expected):
    assert count_worktime(todo_list, workday) == pytest.approx(expected)


def test_count_worktime_default_workday():
    """Если workday не передан, по умолчанию он равен 8."""
    assert count_worktime([["Задача", 3]]) == pytest.approx(5.0)


# ---------- Задание: связь между длительностью курса и числом преподавателей ----------

def make_courses(durations, mentors_counts):
    """Собирает список курсов нужного формата: у каждого курса title, mentors и duration."""
    return [
        {"title": f"Курс {i}", "mentors": [f"Преподаватель {j}" for j in range(count)], "duration": duration}
        for i, (duration, count) in enumerate(zip(durations, mentors_counts))
    ]


# число преподавателей в курсах из задания: 21, 16, 11, 12
MENTORS_COUNTS = [21, 16, 11, 12]


@pytest.mark.parametrize(
    'durations, mentors_counts, expected',
    [
        # связи нет (длительности из задания)
        ([14, 20, 12, 20], MENTORS_COUNTS, (False, [2, 0, 1, 3], [2, 3, 1, 0])),
        # связь есть (вторые длительности из задания)
        ([21, 16, 11, 12], MENTORS_COUNTS, (True, [2, 3, 1, 0], [2, 3, 1, 0])),
        # один курс: связь тривиально есть
        ([10], [5], (True, [0], [0])),
        # пустой список курсов
        ([], [], (True, [], [])),
        # чем длиннее курс, тем больше преподавателей: связь есть
        ([10, 20, 30], [3, 6, 9], (True, [0, 1, 2], [0, 1, 2])),
        # чем длиннее курс, тем меньше преподавателей: связи нет
        ([10, 20, 30], [9, 6, 3], (False, [0, 1, 2], [2, 1, 0])),
    ],
    ids=['связи нет (из задания)', 'связь есть (из задания)', 'один курс', 'пустой список',
         'прямая зависимость', 'обратная зависимость'],
)
def test_check_corr(durations, mentors_counts, expected):
    assert check_corr(make_courses(durations, mentors_counts)) == expected


def test_check_corr_returns_tuple_of_three():
    result = check_corr(make_courses([5, 7], [2, 3]))
    assert isinstance(result, tuple) and len(result) == 3
    assert isinstance(result[0], bool)


# ---------- Задание: подсчёт голосов на выборах ----------

CITIZENS_VOTES = [
    [3, 2, 3, 2, 1, 1, 1, 3, 1, 1],
    [1, 1, 2, 1, 2, 1, 3, 3, 3, 3, 2, 1, 2, 1, 1],
    [1, 2, 2, 3, 2, 1, 1, 3, 2, 3, 2, 2, 3, 3, 1, 2, 1, 3, 3, 1],
    [2, 2, 1, 3, 3, 2, 3, 1, 1, 2, 1, 2, 2, 2, 3],
    [3, 3, 2, 2, 1, 3, 1, 2, 3, 1, 2, 2, 1, 3, 3],
]
SECOND_ROUND = "Нужен второй тур выборов"


@pytest.mark.parametrize(
    'votes, expected',
    list(zip(CITIZENS_VOTES, [1, 1, SECOND_ROUND, 2, 3])),
    ids=[f'набор {i}' for i in range(1, 6)],
)
def test_vote_winner(votes, expected):
    assert vote(votes) == expected


@pytest.mark.parametrize(
    'votes, expected',
    [
        ([1], 1),                          # один голос
        ([1, 2], SECOND_ROUND),            # ничья
        ([2, 2, 2], 2),                    # все голоса за одного
        (['а', 'б', 'а'], 'а'),            # кандидаты не обязательно числа
        ([1, 1, 2, 2, 3, 3], SECOND_ROUND),  # ничья между тремя
    ],
    ids=['один голос', 'ничья двух', 'один кандидат', 'строки', 'ничья трёх'],
)
def test_vote_edge_cases(votes, expected):
    assert vote(votes) == expected


@pytest.mark.parametrize(
    'votes, expected_count',
    [
        ([3, 2, 3, 2, 1, 1, 1, 3, 1, 1], {3: 3, 2: 2, 1: 5}),
        ([1, 2, 2], {1: 1, 2: 2}),
        ([7], {7: 1}),
    ],
)
def test_vote_count_dictionary(votes, expected_count):
    """Функция должна правильно заполнять словарь votes_count (он сохраняется в votes_count_global)."""
    vote(votes)
    assert voting.votes_count_global == expected_count


def test_vote_empty_list_raises():
    """Для пустого списка голосов max() выбрасывает ValueError."""
    with pytest.raises(ValueError):
        vote([])