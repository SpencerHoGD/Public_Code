def chuck(array, n=2):
    length = len(array)
    result = list()
    start = 0

    while(start < length):
        result.append(array[start: start+n] if start+n < length else array[start:])
        start += n

    return result


def sort_by_values(d):
    sorted_values = sorted(d.items(), key=lambda x: x[1])
    return dict(sorted_values)


def split_text(string):
    return string[0], list(string[1:-1]), string[-1]


def capitalize(string, is_capitalize=False):
    if is_capitalize:
        return string[0].upper() + string[1:].lower()
    return string


def n_grams(s, n):
    return [s[start: end] for start, end in zip(range(0, len(s)-n+1), range(n, len(s)+1))]


def func1(l, n):
    return [(x, y, z) for x, y, z in zip([i for i in l if i % 3 == 1], [i for i in l if i % 3 == 2], [i for i in l if i % 3 == 0])]


if __name__ == '__main__':
    l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(list(zip(*[iter(l)] * 3)))
    print(func1(l, len(l)))
