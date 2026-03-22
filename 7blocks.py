"""
Problem: 7 blocks
Initial state: 7 blocks arranged in three stacks ([a,b], [c,d,e], [f,g]).
Goal state: Blocks reorganized into two towers ([a,c,e,g], [b,d,f]).
"""
from aipython.stripsProblem import Planning_problem

from blocks_world_helper import BlocksWorldHelper, blocks_heuristic, solve_and_record

BLOCKS = {"a", "b", "c", "d", "e", "f", "g"}
PROBLEM_NAME = "7 blocks - three stacks into two towers"
EXPERIMENT = "7blocks"

if __name__ == "__main__":
    helper = BlocksWorldHelper(BLOCKS)
    init = helper.create_state([["a", "b"], ["c", "d", "e"], ["f", "g"]])
    goal = helper.create_goal([["a", "c", "e", "g"], ["b", "d", "f"]])
    problem = Planning_problem(helper.domain, init, goal)

    solve_and_record(problem, PROBLEM_NAME, EXPERIMENT)
    solve_and_record(problem, PROBLEM_NAME, EXPERIMENT, heur=blocks_heuristic)
