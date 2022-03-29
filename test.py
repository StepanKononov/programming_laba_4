import numpy as np
import math, random
import matplotlib.pyplot as plt
import random



def mnk(x: list, y: list):
    n = len(x)

    sum_x = sum(x);
    sum_y = sum(y)
    sum_xy = sum(map(lambda x, y: x * y, x, y))
    sum_x2 = sum(map(lambda x: x ** 2, x))

    det_m = np.linalg.det(np.matrix([[sum_x2, sum_x], [sum_x, n]]))
    det_a = np.linalg.det(np.matrix([[sum_xy, sum_x], [sum_y, n]]))
    det_b = np.linalg.det(np.matrix([[sum_x2, sum_xy], [sum_x, sum_y]]))

    a = det_a / det_m
    b = det_b / det_m

    return a, b


def rand_remove(original_data_y):
    deleted_data_y = original_data_y.copy()

    number_deleted_values = len(deleted_data_y) - 200
    values_counter = 0

    while values_counter < number_deleted_values:
        index = random.randint(0, len(deleted_data_y) - 1)
        if deleted_data_y[index] is not None:
            deleted_data_y[index] = None
            values_counter += 1
    return deleted_data_y

def find_nearsts_value(data, index):
    prev_elems_index = [index, None]
    next_elems_index = [index, None]

    while prev_elems_index[0] > 0 and data[prev_elems_index[0]] is None:
        prev_elems_index[0] -= 1
        prev_elems_index[1] = prev_elems_index[0]
        if prev_elems_index[0] > 0 and data[prev_elems_index[0]] is not None:
            prev_elems_index[1] -= 1

            while prev_elems_index[1] > 0 and data[prev_elems_index[1]] is None:
                prev_elems_index[1] -= 1

    while next_elems_index[0] < len(data) and data[next_elems_index[0]] is None:
        next_elems_index[0] += 1
        next_elems_index[1] = next_elems_index[0]
        if next_elems_index[0] < len(data) and data[next_elems_index[0]] is not None:
            next_elems_index[1] += 1
            while next_elems_index[1] < len(data) and data[next_elems_index[1]] is None:
                next_elems_index[1] += 1
    first_index = None
    second_index = None
    if prev_elems_index[0] >= 0 and next_elems_index[0] < len(data):
        if data[prev_elems_index[0]] is not None and data[next_elems_index[0]] is not None:
            first_index = prev_elems_index[0]
            second_index = next_elems_index[0]

            return first_index, second_index

    if prev_elems_index[0] >= 0 and data[prev_elems_index[0]] is None:
        first_index = next_elems_index[0]
        second_index = next_elems_index[1]

        return first_index, second_index

    return prev_elems_index[0], prev_elems_index[1]


def f(x):
    pi = math.pi
    e = math.e
    return np.cos(2 * pi * x) * pow(e, -x)


if True:
    X = np.arange(0, 5, 0.01)
    Y = [f(x) for x in X]

    removed_Y = rand_remove(Y)

    result_Y = removed_Y.copy()

    indicess = [i for i, x in enumerate(removed_Y) if x == None]
    for i in indicess:
        prv, nxt = find_nearsts_value(removed_Y, i)

        a, b = mnk([X[prv], X[nxt]], [removed_Y[prv], removed_Y[nxt]])

        r_y = a * X[i] + b
        result_Y[i] = r_y
        # print(r_y, Y[i])

    plt.figure(figsize=(10, 4))
    plt.suptitle("Восстановление методом винзорирования")
    # plt.figtext(0.5, -0.1, f"Коэфициент отклонения: {coef}")

    plt.subplot(1, 2, 1)
    plt.title("Было")
    # plt.xlabel("Время")
    # plt.ylabel("Температура")
    plt.axis([0, X.max(), -1, 2])
    plt.plot(X, Y, color="#CE7A60")
    plt.scatter(X, Y)

    plt.subplot(1, 2, 2)
    plt.title("Стало")
    # plt.xlabel("Время")
    # plt.ylabel("Температура")
    plt.axis([0, X.max(), -1, 2])
    plt.plot(X, result_Y, color="#FE7A60")
    plt.scatter(X, result_Y)

    plt.show()