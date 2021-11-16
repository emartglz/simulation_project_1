def calculate_average(a, b):
    sum = 0
    for k in a.keys():
        sum += a[k] - b[k]
    return sum / len(a.keys())
