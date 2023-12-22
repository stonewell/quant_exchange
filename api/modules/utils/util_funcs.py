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

def cross(v1, v2, days):
    for i in range(1, days - 1):
        if (all([v1[j] <= v2[j] for j in range(i)])
            and all([v1[j] > v2[j] for j in range(i, days)])):
            return True

    return False
