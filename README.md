# Концепция оценки командного взаимодействия человека на примере командных компьютерных игр

## Идея 

Мы решили выбрать такую модель, при которой человеку в конкретно выбранной игре ставится оценка его командных действий из отрезка [0, 1], исходя из его результатов в этой игре. Мы составили алгоритм, который рассчитывает эту оценку из данных статистики игрока, которую мы можем получить из открытых источников. Для демонстрации мы взяли популярные игры нескольких жанров: MOBA (League of Legends), FPS (CS:GO, Rainbow Six Siege) и Battle Royale (Fortnite, COD:Warzone). Исходя из нашего обширного игрового опыта, мы отобрали те показатели, которые максимально объективно, насколько это возможно, отражают командные навыки игрока и рассчитали, как сильно эти показатели влияют на оценку, а также алгоритм расчета общей оценки человека из совокупности его оценок в разных играх.

## Подсчет по дереву

Принцип работы нашего алгоритма основан на использовании специального корневого дерева для оценки уровня командной игры каждого отдельного игрока p.

Каждый лист L в дереве имеет ассоциированную с ним константу wL, называющуюся Весом листа, со значением лежащем в (0, 1], и функцию fL(p), называющуюся Выражением листа, ограниченную снизу нулём и сверху единицей. Оценкой листа L для игрока p называется функция vL(p) = fL(p) * wL.

Каждый узел ветвления U в дереве имеет ассоциированную с ним константу wU, называющуюся Весом узла ветвления, со значением лежащем в (0, 1], и функцию 
fU(D, p), где D – вектор Оценок всех потомков данного узла, называющуюся Выражением узла ветвления, ограниченную снизу нулём и сверху единицей. Оценкой узла ветвления U для игрока p называется функция vU(p) = fU(D, p) * wU.

Вот функции, которые мы используем:
max(D, p) – наибольшее значение Оценки для игрока p среди D;
sum(D, p) – сумма значений Оценок для игрока p среди D;
n(G) = norm(p, S, G) = pG / SG, где S – Наибольшие значения среди всех наших игроков по всем величинам, p – Игрок, G – Графа в статистике (чтобы превратить значение параметра, лежащее в диапазоне луча, например от нуля до бесконечности, заключить в отрезок).

## О выбранных играх

При составлении дерева на этом этапе мы проанализировали результаты, которые дают различные игры и пришли к выводу, что некоторые дисциплины требуют дальнейшей балансировки и не могут быть включены в проект на данном этапе
