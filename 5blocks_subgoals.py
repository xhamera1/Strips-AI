"""
Problem: 5 blocks with subgoals
Initial state: 5 blocks (a, b, c, d, e) lying separately on the table.
Goal state: All blocks stacked in a single tower (a on b on c on d on e).

Subgoal decomposition:
  Subgoal 1: Place d on e (build the bottom pair)
  Subgoal 2: Place c on d, keeping d on e (bottom three correct)
  Final:     Complete tower a on b on c on d on e
"""
from aipython.stripsProblem import Planning_problem

from blocks_world_helper import (BlocksWorldHelper, blocks_heuristic,
                                 solve_and_record_subgoals)

BLOCKS = {"a", "b", "c", "d", "e"}
PROBLEM_NAME = "5 blocks - scattered into one tower (subgoals)"
EXPERIMENT = "5blocks_subgoals"

if __name__ == "__main__":
    helper = BlocksWorldHelper(BLOCKS)
    init = helper.create_state([["a"], ["b"], ["c"], ["d"], ["e"]])

    subgoal1 = {"d_is_on": "e"}
    subgoal2 = {"c_is_on": "d", "d_is_on": "e"}
    final_goal = helper.create_goal([["a", "b", "c", "d", "e"]])

    subgoals = [subgoal1, subgoal2]

    solve_and_record_subgoals(helper.domain, init, subgoals, final_goal,
                              PROBLEM_NAME, EXPERIMENT)
    solve_and_record_subgoals(helper.domain, init, subgoals, final_goal,
                              PROBLEM_NAME, EXPERIMENT, heur=blocks_heuristic)
