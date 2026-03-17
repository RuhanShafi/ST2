def count_occurrences(lst):
    result = []
    seen = []

    for item in lst:
        if item not in seen:
            count = lst.count(item)
            result.append((item, count))
            seen.append(item)

    return result


data = [1, 2, 2, 3, 4, 4, 5, 1]
print(count_occurrences(data))
