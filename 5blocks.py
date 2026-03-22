"""
Problem 5 klockow
Stan poczatkowy: 5 klockow (a, b, c, d, e) lezy osobno na stole.
Stan docelowy: Wszystkie klocki ulozone w jedna wieze (a na b na c na d na e).
"""
from aipython.stripsProblem import Planning_problem

from blocks_world_helper import BlocksWorldHelper, blocks_heuristic, solve_and_record

BLOCKS = {"a", "b", "c", "d", "e"}
PROBLEM_NAME = "5 klockow - rozproszone w jedna wieze"
EXPERIMENT = "5blocks"

if __name__ == "__main__":
    helper = BlocksWorldHelper(BLOCKS)
    init = helper.create_state([["a"], ["b"], ["c"], ["d"], ["e"]])
    goal = helper.create_goal([["a", "b", "c", "d", "e"]])
    problem = Planning_problem(helper.domain, init, goal)

    solve_and_record(problem, PROBLEM_NAME, EXPERIMENT)
    solve_and_record(problem, PROBLEM_NAME, EXPERIMENT, heur=blocks_heuristic)
