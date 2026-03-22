"""
Problem 6 klockow
Stan poczatkowy: 6 klockow ulozonych w jedna wieze (a na b na c na d na e na f).
Stan docelowy: Wieza calkowicie odwrocona (f na e na d na c na b na a).
"""
from aipython.stripsProblem import Planning_problem

from blocks_world_helper import BlocksWorldHelper, blocks_heuristic, solve_and_record

BLOCKS = {"a", "b", "c", "d", "e", "f"}
PROBLEM_NAME = "6 klockow - odwrocenie wiezy"
EXPERIMENT = "6blocks"

if __name__ == "__main__":
    helper = BlocksWorldHelper(BLOCKS)
    init = helper.create_state([["a", "b", "c", "d", "e", "f"]])
    goal = helper.create_goal([["f", "e", "d", "c", "b", "a"]])
    problem = Planning_problem(helper.domain, init, goal)

    solve_and_record(problem, PROBLEM_NAME, EXPERIMENT)
    solve_and_record(problem, PROBLEM_NAME, EXPERIMENT, heur=blocks_heuristic)
