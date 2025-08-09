from data_schema import Instance, Solution
from ortools.sat.python import cp_model


def solve(instance: Instance) -> Solution:
    """
    Implement your solver for the problem here!
    """
    numbers = instance.numbers
    model = cp_model.CpModel()
    small_bool = [model.NewBoolVar(f"small_{i}") for i in range(len(numbers))]
    big_bool = [model.NewBoolVar(f"big_{i}") for i in range(len(numbers))]
    
    model.add(sum(small_bool) <= 1)
    model.add(sum(small_bool) >= 1)
    model.add(sum(big_bool) <= 1)
    model.add(sum(big_bool) >= 1)

    model.Maximize(sum(x * i for x, i in zip(big_bool, numbers)) - sum(x * i for x, i in zip(small_bool, numbers)))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    #print(numbers)
    assert status == cp_model.OPTIMAL
    a, b = 0, 0
    for i in range(len(numbers)):
        if solver.Value(small_bool[i]) == 1:
            a = numbers[i]
        if solver.Value(big_bool[i]) == 1:
            b = numbers[i]

    return Solution(
        number_a=a,
        number_b=b,
        distance=b-a,
    )
