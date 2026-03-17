import timeit

# -----------------------------
# RECURSIVE FUNCTIONS
# -----------------------------

def sum_recursive(n):
    if n == 1:
        return 1
    return n + sum_recursive(n - 1)


def fibonacci_recursive(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def factorial_recursive(n):
    if n == 0:
        return 1
    return n * factorial_recursive(n - 1)


# -----------------------------
# ITERATIVE FUNCTIONS
# -----------------------------

def sum_iterative(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


def fibonacci_iterative(n):
    if n <= 0:
        return 0
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def factorial_iterative(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


# -----------------------------
# BENCHMARKING
# -----------------------------

def benchmark():
    test_values = [10, 20, 30]  # different data sizes

    for n in test_values:
        print(f"\n===== Testing n = {n} =====")

        # SUM
        sum_rec_time = timeit.timeit(lambda: sum_recursive(n), number=1000)
        sum_itr_time = timeit.timeit(lambda: sum_iterative(n), number=1000)

        print(f"Sum Recursive:  {sum_rec_time:.6f}")
        print(f"Sum Iterative:  {sum_itr_time:.6f}")

        # FACTORIAL
        fact_rec_time = timeit.timeit(lambda: factorial_recursive(n), number=1000)
        fact_itr_time = timeit.timeit(lambda: factorial_iterative(n), number=1000)

        print(f"Factorial Recursive: {fact_rec_time:.6f}")
        print(f"Factorial Iterative: {fact_itr_time:.6f}")

        # FIBONACCI 
        fib_rec_time = timeit.timeit(lambda: fibonacci_recursive(n), number=10)
        fib_itr_time = timeit.timeit(lambda: fibonacci_iterative(n), number=1000)

        print(f"Fibonacci Recursive: {fib_rec_time:.6f}")
        print(f"Fibonacci Iterative: {fib_itr_time:.6f}")


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":
    benchmark()