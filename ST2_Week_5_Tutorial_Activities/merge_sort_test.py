import random


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# TESTING
sizes = [10, 100, 1000]

for size in sizes:
    data = [random.randint(1, 1000) for _ in range(size)]
    sorted_data = merge_sort(data)

    print(f"\nSize: {size}")
    print("First 10 sorted elements:", sorted_data[:10])