import random


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr


# TESTING
sizes = [10, 100, 1000]

for size in sizes:
    data = [random.randint(1, 1000) for _ in range(size)]
    sorted_data = insertion_sort(data)

    print(f"\nSize: {size}")
    print("First 10 sorted elements:", sorted_data[:10])