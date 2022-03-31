import numpy as np
import random


def mnk(x: list, y: list):
    n = len(x)

    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(map(lambda x, y: x * y, x, y))
    sum_x2 = sum(map(lambda x: x ** 2, x))

    det_m = np.linalg.det(np.matrix([[sum_x2, sum_x], [sum_x, n]]))
    det_a = np.linalg.det(np.matrix([[sum_xy, sum_x], [sum_y, n]]))
    det_b = np.linalg.det(np.matrix([[sum_x2, sum_xy], [sum_x, sum_y]]))

    a = det_a / det_m
    b = det_b / det_m

    return a, b


def rand_remove(original_data_y, amount_del):
    deleted_data_y = original_data_y.copy()

    amount_deleted_values = len(deleted_data_y) * amount_del // 100
    values_counter = 0
    for i in range(len(deleted_data_y)):
        if np.isnan(deleted_data_y[i]):
            values_counter += 1

    while values_counter < amount_deleted_values:
        index = random.randint(0, len(deleted_data_y) - 1)
        if not np.isnan(deleted_data_y[index]):
            deleted_data_y[index] = np.nan
            values_counter += 1
    return deleted_data_y


def find_nearest_value(data, index, none=np.nan):
    prev_elems_index = [index, none]
    next_elems_index = [index, none]

    while prev_elems_index[0] > 0 and data[prev_elems_index[0]] is none:
        prev_elems_index[0] -= 1
        prev_elems_index[1] = prev_elems_index[0]
        if prev_elems_index[0] > 0 and data[prev_elems_index[0]] is not none:
            prev_elems_index[1] -= 1

            while prev_elems_index[1] > 0 and data[prev_elems_index[1]] is none:
                prev_elems_index[1] -= 1

    while next_elems_index[0] < len(data) and data[next_elems_index[0]] is none:
        next_elems_index[0] += 1
        next_elems_index[1] = next_elems_index[0]
        if next_elems_index[0] < len(data) and data[next_elems_index[0]] is not none:
            next_elems_index[1] += 1
            while next_elems_index[1] < len(data) and data[next_elems_index[1]] is none:
                next_elems_index[1] += 1
    first_index = none
    second_index = none
    if prev_elems_index[0] >= 0 and next_elems_index[0] < len(data):
        if data[prev_elems_index[0]] is not none and data[next_elems_index[0]] is not none:
            first_index = prev_elems_index[0]
            second_index = next_elems_index[0]

            return first_index, second_index

    if prev_elems_index[0] >= 0 and data[prev_elems_index[0]] is none:
        first_index = next_elems_index[0]
        second_index = next_elems_index[1]

        return first_index, second_index

    return prev_elems_index[0], prev_elems_index[1]


def mnk_resolve_data(data_Y, data_X):
    result_Y = data_Y.copy()

    indicess = [i for i, x in enumerate(data_Y) if np.isnan(x)]
    print(indicess)
    for i in indicess:
        prv, nxt = find_nearest_value(data_Y, i)

        a, b = mnk([data_X[prv], data_X[nxt]], [data_Y[prv], data_Y[nxt]])

        r_y = a * data_X[i] + b
        result_Y[i] = r_y
    return result_Y


def winsorizing_resolve_data(data_Y):
    result_Y = data_Y.copy()
    if np.isnan(result_Y[0]):
        for i in range(1, len(result_Y)):
            if not np.isnan(result_Y[i]):
                result_Y[0] = result_Y[i]
    for i in range(1, len(result_Y)):
        if np.isnan(result_Y[i]):
            result_Y[i] = result_Y[i - 1]
    return result_Y


def get_corrcoef(ar1):
    ar1[0] = ar1[0][:min(len(ar1[0]), len(ar1[1]))]
    ar1[1] = ar1[1][:min(len(ar1[0]), len(ar1[1]))]
    return np.corrcoef(ar1)[0][1]


def c_recovery(data_Y, big_data, ticker):
    coref_dict = dict()
    for key in big_data:
        if key == ticker:
            continue
        coref_dict[key] = get_corrcoef([data_Y, big_data[key]])
    coref_dict = dict(sorted(coref_dict.items(), key=lambda x: x[1]))
    # Я конечно нашёл ряд с макс кор но наверное нужно найти коэф зависимости

    for i in range(len(data_Y)):
        if np.isnan(data_Y[i]):
            for key in coref_dict:
                if i < len(big_data[key]) and not np.isnan(big_data[key][i]):
                    delta = 1
                    for f, s in zip(data_Y, big_data[key]):
                        if not np.isnan(f) and not np.isnan(s):
                            delta = f / s
                            break
                    data_Y[i] = big_data[key][i] * delta

    return data_Y


def MA(points, deviation):
    n = len(points)
    period = n // 5 + 1
    smoothed_points = []
    deviation /= 100

    for i in range(0, period):
        slice_period = points[0: i]
        if len(slice_period) > 0:
            cur_point = sum(slice_period) / len(slice_period)
            smoothed_points.append(cur_point)
        else:
            smoothed_points.append(points[i])

    for i in range(period, n):
        for step in range(period, 2, -1):
            slice_Y = points[i - step:i]
            cur_point = sum(slice_Y) / len(slice_Y)

            if abs(points[i] - cur_point) / max(cur_point, points[i]) <= deviation or step == 3:
                smoothed_points.append(cur_point)
                break

    return smoothed_points


def WMA(points, deviation):
    deviation /= 100
    smoothed_points = []
    for point in points:
        try:
            if smoothed_points:
                previous = smoothed_points[-1]
                smoothed_points.append(previous * deviation + point * (1 - deviation))
            else:
                smoothed_points.append(point)
        except ValueError:
            print("WMA ERROR")
            pass
    return smoothed_points


def weightedmovingaverage(Data, period):
    weighted = []
    for i in range(len(Data)):
        try:
            total = np.arange(1, period + 1, 1)
            matrix = Data[i - period + 1: i + 1, 3:4]
            matrix = np.ndarray.flatten(matrix)
            matrix = total * matrix
            wma = (matrix.sum()) / (total.sum())
            weighted = np.append(weighted, wma)
        except ValueError:
            pass
    return weighted
