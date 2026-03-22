"""
Problem: 5 blocks
Initial state: 5 blocks (a, b, c, d, e) lying separately on the table.
Goal state: All blocks stacked in a single tower (a on b on c on d on e).
"""
from aipython.stripsProblem import Planning_problem

from blocks_world_helper import BlocksWorldHelper, blocks_heuristic, solve_and_record

BLOCKS = {"a", "b", "c", "d", "e"}
PROBLEM_NAME = "5 blocks - scattered into one tower"
EXPERIMENT = "5blocks"

if __name__ == "__main__":
    helper = BlocksWorldHelper(BLOCKS)
    init = helper.create_state([["a"], ["b"], ["c"], ["d"], ["e"]])
    goal = helper.create_goal([["a", "b", "c", "d", "e"]])
    problem = Planning_problem(helper.domain, init, goal)

    solve_and_record(problem, PROBLEM_NAME, EXPERIMENT)
    solve_and_record(problem, PROBLEM_NAME, EXPERIMENT, heur=blocks_heuristic)
