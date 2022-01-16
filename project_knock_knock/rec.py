def fibonacci_of(n):
    if n in {0, 1}:  # Base case
        return n
    return fibonacci_of(n - 1) + fibonacci_of(n - 2)  # Recursive case


fibonacci_of(5)


def test():
    return "hi"


print(test())


def rec(pi):
    pi.append()
