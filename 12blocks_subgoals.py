"""
Problem: 12 blocks - single tower split into two interleaved towers
Initial: One tower [a,b,c,d,e,f,g,h,i,j,k,l] (a on top, l on bottom)
Goal:    Two towers [a,c,e,g,i,k] and [b,d,f,h,j,l]
Requires ~21 actions.
"""
from blocks_world_helper import (BlocksWorldHelper, blocks_heuristic,
                                 solve_and_record_subgoals)

BLOCKS = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"}
PROBLEM_NAME = "12 blocks - tower to two interleaved towers"
EXPERIMENT = "12blocks_subgoals"

if __name__ == "__main__":
    helper = BlocksWorldHelper(BLOCKS)
    init = helper.create_state([["a", "b", "c", "d", "e", "f",
                                  "g", "h", "i", "j", "k", "l"]])

    subgoals = [
        {"a_is_on": "table", "b_is_on": "table", "c_is_on": "table",
         "d_is_on": "table", "e_is_on": "table", "f_is_on": "table"},
        {"g_is_on": "table", "h_is_on": "table",
         "i_is_on": "table", "j_is_on": "table", "k_is_on": "table"},
        {"i_is_on": "k", "k_is_on": "table", "j_is_on": "l"},
        {"g_is_on": "i", "h_is_on": "j", "i_is_on": "k", "j_is_on": "l"},
        {"e_is_on": "g", "f_is_on": "h", "g_is_on": "i", "h_is_on": "j"},
    ]

    final_goal = helper.create_goal([["a", "c", "e", "g", "i", "k"],
                                      ["b", "d", "f", "h", "j", "l"]])

    solve_and_record_subgoals(helper.domain, init, subgoals, final_goal,
                              PROBLEM_NAME, EXPERIMENT)
    solve_and_record_subgoals(helper.domain, init, subgoals, final_goal,
                              PROBLEM_NAME, EXPERIMENT, heur=blocks_heuristic)
