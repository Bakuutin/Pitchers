Программа ищет оптимальное решение для произвольной задачи на переливание двух кувшинов.

Пример задачи:
  C помощью двух сосудов вместимостью 3 и 5 литров получить в одном из сосудов 4 литра
  
Пример работы программы:
  Введите через пробел объёмы двух кувшинов: 3 5
  Введите желаемый объём: 4
  Требуется шагов: 6
  (0, 0) start
  (0, 5) fill
  (3, 2) transfer
  (0, 2) empty
  (2, 0) transfer
  (2, 5) fill
  (3, 4) transfer
  
Ещё пример:
  Введите через пробел объёмы двух кувшинов: 13 6
  Введите желаемый объём: 3
  Требуется шагов: 16
  (0, 0) start
  (13, 0) fill
  (7, 6) transfer
  (7, 0) empty
  (1, 6) transfer
  (1, 0) empty
  (0, 1) transfer
  (13, 1) fill
  (8, 6) transfer
  (8, 0) empty
  (2, 6) transfer
  (2, 0) empty
  (0, 2) transfer
  (13, 2) fill
  (9, 6) transfer
  (9, 0) empty
  (3, 6) transfer