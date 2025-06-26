
import pytest


@pytest.fixture
def get_fib_stop():
    i = 6
    return i


def fibonacci(i, memo):
    if i < 2:
        return i
    if i not in memo:
        memo[i] = fibonacci(i-2, memo)+fibonacci(i-1, memo)
    return memo[i]


@pytest.mark.math
def test_fibonacci(get_fib_stop):
    # 0-indexed
    assert fibonacci(get_fib_stop-1, dict()) == 5

# 0 1 1 2 3 5


@pytest.mark.math
@pytest.mark.parametrize("i, result", [(1, 0), (2, 1), (3, 1), (4, 2), (5, 3), (6, 5)])
def test_fibonacci_sequence(i, result):
    memo = {}
    assert fibonacci(i-1, memo) == result
