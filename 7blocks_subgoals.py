"""
Problem: 7 blocks with subgoals
Initial state: Three stacks [a,b], [c,d,e], [f,g].
Goal state: Two towers [a,c,e,g] and [b,d,f].

Subgoal decomposition:
  Subgoal 1: Place e on g and f on table (start building first tower base,
             free up f for second tower)
  Subgoal 2: Place c on e and d on f (extend both towers)
  Final:     Complete both towers: a on c on e on g, b on d on f
"""
from aipython.stripsProblem import Planning_problem

from blocks_world_helper import (BlocksWorldHelper, blocks_heuristic,
                                 solve_and_record_subgoals)

BLOCKS = {"a", "b", "c", "d", "e", "f", "g"}
PROBLEM_NAME = "7 blocks - three stacks into two towers (subgoals)"
EXPERIMENT = "7blocks_subgoals"

if __name__ == "__main__":
    helper = BlocksWorldHelper(BLOCKS)
    init = helper.create_state([["a", "b"], ["c", "d", "e"], ["f", "g"]])

    subgoal1 = {"e_is_on": "g", "f_is_on": "table"}
    subgoal2 = {"c_is_on": "e", "d_is_on": "f", "e_is_on": "g"}
    final_goal = helper.create_goal([["a", "c", "e", "g"], ["b", "d", "f"]])

    subgoals = [subgoal1, subgoal2]

    solve_and_record_subgoals(helper.domain, init, subgoals, final_goal,
                              PROBLEM_NAME, EXPERIMENT)
    solve_and_record_subgoals(helper.domain, init, subgoals, final_goal,
                              PROBLEM_NAME, EXPERIMENT, heur=blocks_heuristic)
