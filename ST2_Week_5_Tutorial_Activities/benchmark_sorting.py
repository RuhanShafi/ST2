import random
import timeit


# MERGE SORT
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))


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


# INSERTION SORT
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr


# BENCHMARK
sizes = [100, 1000, 5000]

for size in sizes:
    data = [random.randint(1, 10000) for _ in range(size)]

    insertion_time = timeit.timeit(
        lambda: insertion_sort(data[:]), number=5
    )

    merge_time = timeit.timeit(
        lambda: merge_sort(data[:]), number=5
    )

    print(f"\nSize: {size}")
    print(f"Insertion Sort: {insertion_time:.6f} sec")
    print(f"Merge Sort:     {merge_time:.6f} sec")