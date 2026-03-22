"""
Problem: 14 blocks - single tower split into three interleaved towers
Initial: One tower [a,b,c,d,e,f,g,h,i,j,k,l,m,n] (a on top, n on bottom)
Goal:    Three towers [a,d,g,j,m], [b,e,h,k,n], [c,f,i,l]
Requires ~24 actions.
"""
from blocks_world_helper import (BlocksWorldHelper, blocks_heuristic,
                                 solve_and_record_subgoals)

BLOCKS = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n"}
PROBLEM_NAME = "14 blocks - tower to three interleaved towers"
EXPERIMENT = "14blocks_subgoals"

if __name__ == "__main__":
    helper = BlocksWorldHelper(BLOCKS)
    init = helper.create_state([["a", "b", "c", "d", "e", "f", "g",
                                  "h", "i", "j", "k", "l", "m", "n"]])

    subgoals = [
        {"a_is_on": "table", "b_is_on": "table", "c_is_on": "table",
         "d_is_on": "table", "e_is_on": "table", "f_is_on": "table",
         "g_is_on": "table"},
        {"h_is_on": "table", "i_is_on": "table", "j_is_on": "table",
         "k_is_on": "table", "l_is_on": "table", "m_is_on": "table"},
        {"m_is_on": "table", "k_is_on": "n", "l_is_on": "table",
         "n_is_on": "table"},
        {"j_is_on": "m", "h_is_on": "k", "i_is_on": "l",
         "m_is_on": "table", "k_is_on": "n", "l_is_on": "table"},
        {"g_is_on": "j", "e_is_on": "h", "f_is_on": "i",
         "j_is_on": "m", "h_is_on": "k", "i_is_on": "l"},
    ]

    final_goal = helper.create_goal([["a", "d", "g", "j", "m"],
                                      ["b", "e", "h", "k", "n"],
                                      ["c", "f", "i", "l"]])

    solve_and_record_subgoals(helper.domain, init, subgoals, final_goal,
                              PROBLEM_NAME, EXPERIMENT)
    solve_and_record_subgoals(helper.domain, init, subgoals, final_goal,
                              PROBLEM_NAME, EXPERIMENT, heur=blocks_heuristic)
