"""
Problem: 6 blocks
Initial state: Two stacks - a tower of 5 blocks [a,b,c,d,e] and a single block [f] on the table.
Goal state: All 6 blocks in one tower [a,b,c,d,e,f] (a on top, f on bottom).
"""
from aipython.stripsProblem import Planning_problem

from blocks_world_helper import BlocksWorldHelper, blocks_heuristic, solve_and_record

BLOCKS = {"a", "b", "c", "d", "e", "f"}
PROBLEM_NAME = "6 blocks - merge tower with single block"
EXPERIMENT = "6blocks"

if __name__ == "__main__":
    helper = BlocksWorldHelper(BLOCKS)
    init = helper.create_state([["a", "b", "c", "d", "e"], ["f"]])
    goal = helper.create_goal([["a", "b", "c", "d", "e", "f"]])
    problem = Planning_problem(helper.domain, init, goal)

    solve_and_record(problem, PROBLEM_NAME, EXPERIMENT)
    solve_and_record(problem, PROBLEM_NAME, EXPERIMENT, heur=blocks_heuristic)
