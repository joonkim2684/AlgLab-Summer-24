import itertools
import math
from typing import List

from data_schema import Instance, Item, Solution
from ortools.sat.python.cp_model import FEASIBLE, OPTIMAL, CpModel, CpSolver


class MultiKnapsackSolver:
    """
    This class can be used to solve the Multi-Knapsack problem
    (also the standard knapsack problem, if only one capacity is used).

    Attributes:
    - instance (Instance): The multi-knapsack instance
        - items (List[Item]): a list of Item objects representing the items to be packed.
        - capacities (List[int]): a list of integers representing the capacities of the knapsacks.
    - model (CpModel): a CpModel object representing the constraint programming model.
    - solver (CpSolver): a CpSolver object representing the constraint programming solver.
    """

    def __init__(self, instance: Instance):
        """
        Initialize the solver with the given Multi-Knapsack instance.

        Args:
        - instance (Instance): an Instance object representing the Multi-Knapsack instance.
        """
        self.items = instance.items
        self.capacities = instance.capacities
        self.model = CpModel()
        self.solver = CpSolver()
        self.solver.parameters.log_search_progress = True
        # TODO: Implement me!

        self.ks = []

        for k in range(len(self.capacities)):
            self.ks.append([self.model.NewBoolVar(f"ks_{k}_{i}") for i in range(len(self.items))])
            self.model.add(sum(x * i.weight for x, i in zip(self.ks[k], self.items)) <= self.capacities[k])

        for i in range(len(self.items)):
            self.model.add(sum(self.ks[k][i] for k in range(len(self.capacities))) <= 1)

        self.model.Maximize(sum([sum(x * i.value for x, i in zip(self.ks[k], self.items)) for k in range(len(self.capacities))]))


    def solve(self, timelimit: float = math.inf) -> Solution:
        """
        Solve the Multi-Knapsack instance with the given time limit.

        Args:
        - timelimit (float): time limit in seconds for the cp-sat solver.

        Returns:
        - Solution: a list of lists of Item objects representing the items packed in each knapsack
        """
        # handle given time limit
        if timelimit <= 0.0:
            return Solution(knapsacks=[])  # empty solution
        elif timelimit < math.inf:
            self.solver.parameters.max_time_in_seconds = timelimit
        # TODO: Implement me!
        status = self.solver.Solve(self.model)
        
        sol = []
        for k in range(len(self.capacities)):
            ks = [i for i, x in zip(self.items, self.ks[k]) if self.solver.Value(x)]
            sol.append(ks)

        return Solution(knapsacks=sol)  # empty solution
