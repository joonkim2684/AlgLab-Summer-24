from data_schema import Instance, Solution


def solve(instance: Instance) -> Solution:
    """
    Implement your solver for the problem here!
    """
    numbers = instance.numbers
    a = min(numbers)
    b = max(numbers)
    return Solution(
        number_a=a,
        number_b=b,
        distance=b-a,
    )
