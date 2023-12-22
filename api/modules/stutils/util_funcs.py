import math

def delta_change(values):
    l = len(values)

    if l == 0:
        return []

    if l == 1:
        return [0]

    last = values[0]

    results = []

    for i in range(1, l):
        if last == 0:
            results.append(100)
        else:
            v = (values[i] - last) * 100 / last
            results.append(v)

        last = values[i]

    return results

def mo(values, group_count = 10):
    groups = []

    for i in range(0, group_count + 1):
        groups.append(0)

    count = len(values)

    if not values:
        return []

    max_v = max(values)
    min_v = min(values)

    delta = (max_v - min_v ) / group_count

    for i in range(0, count):
        index = math.trunc((values[i] - min_v) / delta)
        groups[index] += 1

    result = [min_v, delta]

    for i in range(0, group_count + 1):
        result.append(float(groups[i]) * 100 / count)

    return result

def normalize_ma(values):
    l = len(values)

    if l == 0:
        return []

    if l == 1:
        return [1]

    last = values[0]

    results = [1]

    for i in range(1, l):
        if last == 0:
            results.append(1)
        else:
            v = values[i] / last
            results.append(v)

    assert len(results) == l,"normalize fail"
    return results
