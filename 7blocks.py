"""
Problem 7 klockow
Stan poczatkowy: 7 klockow ulozonych w trzech stosach ([a,b], [c,d,e], [f,g]).
Stan docelowy: Klocki przeorganizowane w dwie wieze ([a,c,e,g], [b,d,f]).
"""
from aipython.stripsProblem import Planning_problem

from blocks_world_helper import BlocksWorldHelper, blocks_heuristic, solve_and_record

BLOCKS = {"a", "b", "c", "d", "e", "f", "g"}
PROBLEM_NAME = "7 klockow - trzy stosy w dwie wieze"
EXPERIMENT = "7blocks"

if __name__ == "__main__":
    helper = BlocksWorldHelper(BLOCKS)
    init = helper.create_state([["a", "b"], ["c", "d", "e"], ["f", "g"]])
    goal = helper.create_goal([["a", "c", "e", "g"], ["b", "d", "f"]])
    problem = Planning_problem(helper.domain, init, goal)

    solve_and_record(problem, PROBLEM_NAME, EXPERIMENT)
    solve_and_record(problem, PROBLEM_NAME, EXPERIMENT, heur=blocks_heuristic)
