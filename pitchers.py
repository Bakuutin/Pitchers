"""
Программа ищет оптимальное решение для задачи про два кувшина
Для работы требуется Python 3
"""
from enum import Enum


class Action(Enum):
    """
    Действия с кувшинами
    """
    empty = 0
    fill = 1
    transfer = 2
    start = 3


def get_pitchers_volume():
    """
    Возвращает список из целочисленных значений объёмов кувшинов
    """
    while True:  # pitchers_volume это list из целых чисел, полученных разбиением вводимой строки
        pitchers_volume = list(int(pitcher) for pitcher in input("Введите через пробел объёмы двух кувшинов: ").split())

        if len(pitchers_volume) != 2:  # Мы рассматриваем только случаи с двумя кувшинами
            print('Айайай! Попробуйте заново.')
        else:
            return pitchers_volume


def get_target():
    """
    Возвращает целочисленный желаемый объём
    """
    return int(input("Введите желаемый объём: "))


def greatest_common_divisor(a, b):
    """
    Считает наибольший общий делитель.
    """
    while b:
        a, b = b, a % b
    return a


def make_edges(i, j, i_max, j_max):
    """
    Создаёт список из всех исходящих ветвей графа в точке (i, j)
    Где i и j — наполненность первого и второго кувшинов
    """
    edges = dict()

    # Если кувшины не пусты, их можно опустошить
    if i != 0:
        edges[(0, j)] = Action.empty
    if j != 0:
        edges[(i, 0)] = Action.empty

    # Если кувшины не полные, их можно наполнить
    if i != i_max:
        edges[(i_max, j)] = Action.fill
    if j != j_max:
        edges[(i, j_max)] = Action.fill

    # Из непустого кувшина можно перелить в неполный
    if i != 0 and j_max-j >= i:
        edges[(0, j+i)] = Action.transfer
    if j != 0 and i_max-i >= j:
        edges[(i+j, 0)] = Action.transfer

    # Причем, если в неполном не хватит места,
    # то оба кувшина останутся непустыми
    if j != 0 and 0 < i_max-i < j:
        edges[(i_max, j - (i_max-i))] = Action.transfer
    if i != 0 and 0 < j_max-j < i:
        edges[(i - (j_max-j), j_max)] = Action.transfer
    return edges


def make_pitchers_graph(pitchers_volume):
    """
    Создаёт словарь, в котором ключи — все комбинации наполненности кувшинов,
    а значения — возможные переходы из каждой комбинации
    """
    pitchers_graph = dict()
    gcd = greatest_common_divisor(pitchers_volume[0], pitchers_volume[1])
    for i in range(0, int(pitchers_volume[0]/gcd)+1):      # Найдём наименьшее общее кратное у объёмов кувшинов
        for j in range(0, int(pitchers_volume[1]/gcd)+1):  # И поделим каждый из объёмов на него, для оптимизации
            pitchers_graph[(i*gcd, j*gcd)] = make_edges(i*gcd, j*gcd, pitchers_volume[0], pitchers_volume[1])
    return pitchers_graph


def dijkstra(graph, start_node, target):
    """
    Находит кратчайший путь в графе
    """
    distance = dict.fromkeys(graph, float('inf'))
    path = dict()
    path[start_node] = [[[start_node], [Action.start]]]  # Путь записывается в виде словаря, в котором к каждому из
    distance[start_node] = 0                           # имён узлов сосоставляется list из предыдущих узлов
    node_set = set(graph)                              # с добавлением типа действия с кувшинами
    targets_list = [node for node in node_set                   # Цели хранятся как list из всех узлов, которые
                    if node[0] == target or node[1] == target]  # подходят в качестве финиша

    while node_set:
        node = min(node_set, key=distance.get)
        if node in targets_list and node in path:  # Как только нашли подходящий узел — выходим. Поскольку мы ищем
            return path[node]                      # от точки (0, 0), а вес каждого ребра считаем одинаковым,
        node_set.remove(node)                      # то первый найденный узел и будет оптимальным
        for child_node in graph[node].keys():
            if distance[child_node] >= distance[node] + 1:  # Вес каждого ребра считаем за единицу
                distance[child_node] = distance[node] + 1
                path[child_node] = list()
                path[child_node].extend(path[node])     # Путь до нового узла состоит из пути до его родителя
                path[child_node].append([[child_node],  # плюс сам переход
                                         [graph[node].get(child_node)]])  # с добавлением типа действия


def show_answer(path, target):
    """
    Выводит ответ в человекочитаемом виде
    """
    if path is not None:
        print('Требуется шагов: '+str(len(path)-1))
        for node in path:
            print(node[0][0], end=' ')
            print(node[1][0].name)
    else:
        print('Нельзя получить '+str(target)+'л., имея только данные кувшины.')


pitchers_volume = get_pitchers_volume()  # Получаем с клавиатуры объёмы кувшинов
target_node = get_target()               # И желаемый объём
start_node = (0, 0)  # Начинаем с пустых кувшинов
pitchers_graph = make_pitchers_graph(pitchers_volume)  # Создаём граф из всех состояний кувшинов
path = dijkstra(pitchers_graph, start_node, target_node)  # Находим кратчайший путь
show_answer(path, target_node)  # Выводим результат