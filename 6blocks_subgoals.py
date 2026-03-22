"""
Problem: 6 blocks with subgoals
Initial state: Tower of 5 [a,b,c,d,e] and a single block [f] on the table.
Goal state: All 6 blocks in one tower [a,b,c,d,e,f] (a on top, f on bottom).

Subgoal decomposition:
  Subgoal 1: Place e on f (requires dismantling the 5-block tower first)
  Subgoal 2: Place d on e and c on d (rebuild the middle section)
  Final:     Complete tower a on b on c on d on e on f
"""
from aipython.stripsProblem import Planning_problem

from blocks_world_helper import (BlocksWorldHelper, blocks_heuristic,
                                 solve_and_record_subgoals)

BLOCKS = {"a", "b", "c", "d", "e", "f"}
PROBLEM_NAME = "6 blocks - merge tower with single block (subgoals)"
EXPERIMENT = "6blocks_subgoals"

if __name__ == "__main__":
    helper = BlocksWorldHelper(BLOCKS)
    init = helper.create_state([["a", "b", "c", "d", "e"], ["f"]])

    subgoal1 = {"e_is_on": "f"}
    subgoal2 = {"d_is_on": "e", "c_is_on": "d", "e_is_on": "f"}
    final_goal = helper.create_goal([["a", "b", "c", "d", "e", "f"]])

    subgoals = [subgoal1, subgoal2]

    solve_and_record_subgoals(helper.domain, init, subgoals, final_goal,
                              PROBLEM_NAME, EXPERIMENT)
    solve_and_record_subgoals(helper.domain, init, subgoals, final_goal,
                              PROBLEM_NAME, EXPERIMENT, heur=blocks_heuristic)
