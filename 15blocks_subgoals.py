"""
Problem: 15 blocks - five stacks of 3 rearranged into three stacks of 5
Initial: Five stacks [a,b,c], [d,e,f], [g,h,i], [j,k,l], [m,n,o]
Goal:    Three stacks [a,e,i,l,o], [b,f,j,m,c], [d,h,k,n,g]
Requires ~22 actions (complete rearrangement of all blocks).
"""
from blocks_world_helper import (BlocksWorldHelper, blocks_heuristic,
                                 solve_and_record_subgoals)

BLOCKS = {"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o"}
PROBLEM_NAME = "15 blocks - five stacks of 3 to three stacks of 5"
EXPERIMENT = "15blocks_subgoals"

if __name__ == "__main__":
    helper = BlocksWorldHelper(BLOCKS)
    init = helper.create_state([["a","b","c"], ["d","e","f"],
                                 ["g","h","i"], ["j","k","l"], ["m","n","o"]])

    subgoals = [
        {"a_is_on":"table", "b_is_on":"table", "d_is_on":"table",
         "e_is_on":"table", "g_is_on":"table", "h_is_on":"table",
         "j_is_on":"table", "k_is_on":"table", "m_is_on":"table",
         "n_is_on":"table"},
        {"l_is_on":"o", "o_is_on":"table",
         "m_is_on":"c", "c_is_on":"table",
         "n_is_on":"g", "g_is_on":"table"},
        {"i_is_on":"l", "j_is_on":"m", "k_is_on":"n",
         "l_is_on":"o", "m_is_on":"c", "n_is_on":"g"},
        {"e_is_on":"i", "f_is_on":"j", "h_is_on":"k",
         "i_is_on":"l", "j_is_on":"m", "k_is_on":"n"},
    ]

    final_goal = helper.create_goal([["a","e","i","l","o"],
                                      ["b","f","j","m","c"],
                                      ["d","h","k","n","g"]])

    solve_and_record_subgoals(helper.domain, init, subgoals, final_goal,
                              PROBLEM_NAME, EXPERIMENT)
    solve_and_record_subgoals(helper.domain, init, subgoals, final_goal,
                              PROBLEM_NAME, EXPERIMENT, heur=blocks_heuristic)
