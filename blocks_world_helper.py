import os
import sys
import time
import threading
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "aipython"))

from aipython.searchMPP import SearcherMPP
from aipython.stripsForwardPlanner import Forward_STRIPS
from aipython.stripsProblem import create_blocks_world


class BlocksWorldHelper:

    def __init__(self, blocks):
        self.blocks = set(blocks)
        self.domain = create_blocks_world(self.blocks)

    def create_state(self, stacks):
        state = {}
        for block in self.blocks:
            state[f"{block}_is_on"] = "table"
            state[f"clear_{block}"] = True

        for stack in stacks:
            for i in range(len(stack) - 1):
                state[f"{stack[i]}_is_on"] = stack[i + 1]
                state[f"clear_{stack[i + 1]}"] = False
            state[f"{stack[-1]}_is_on"] = "table"

        return state

    def create_goal(self, stacks):
        goal = {}
        for stack in stacks:
            for i in range(len(stack) - 1):
                goal[f"{stack[i]}_is_on"] = stack[i + 1]
            goal[f"{stack[-1]}_is_on"] = "table"
        return goal


def blocks_heuristic(state, goal):
    return sum(1 for prop, value in goal.items() if state.get(prop) != value)


def extract_actions(solution_path):
    actions = []
    current = solution_path
    while current.arc is not None:
        if current.arc.action:
            actions.append(current.arc.action.name)
        current = current.initial
    actions.reverse()
    return actions


def solve(problem, heur=None, timeout_seconds=300):
    if heur:
        search_problem = Forward_STRIPS(problem, heur=heur)
    else:
        search_problem = Forward_STRIPS(problem)

    searcher = SearcherMPP(search_problem)
    searcher.max_display_level = 0

    result_container = [None]

    def run_search():
        result_container[0] = searcher.search()

    thread = threading.Thread(target=run_search)
    thread.daemon = True

    start_time = time.time()
    thread.start()
    thread.join(timeout=timeout_seconds)
    elapsed = time.time() - start_time

    timed_out = thread.is_alive()
    solution_path = None if timed_out else result_container[0]

    if timed_out:
        elapsed = timeout_seconds

    actions = extract_actions(solution_path) if solution_path else []
    expanded = searcher.num_expanded

    return {
        "solved": solution_path is not None,
        "time": elapsed,
        "actions": actions,
        "num_actions": len(actions),
        "num_expanded": expanded,
    }


def solve_and_record(problem, problem_name, experiment_name, heur=None, timeout_seconds=300):
    print(f"\n{'='*60}")
    print(f"Experiment: {experiment_name}")
    print(f"Problem: {problem_name}")
    heur_label = heur.__name__ if heur else "none"
    print(f"Heuristic: {heur_label}")
    print(f"{'='*60}")

    result = solve(problem, heur=heur, timeout_seconds=timeout_seconds)

    if result["solved"]:
        print(f"Solution found in {result['time']:.4f}s")
        print(f"Number of actions: {result['num_actions']}")
        print(f"Expanded states: {result['num_expanded']}")
        print("Action plan:")
        for i, action in enumerate(result["actions"], 1):
            print(f"  {i}. {action}")
    else:
        print(f"No solution found (timeout {timeout_seconds}s)")
        print(f"Expanded states: {result['num_expanded']}")

    _save_result(experiment_name, problem_name, heur_label, result)

    return result


def _save_result(experiment_name, problem_name, heur_label, result):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{experiment_name}_{heur_label}_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Experiment: {experiment_name}\n")
        f.write(f"Problem: {problem_name}\n")
        f.write(f"Heuristic: {heur_label}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*50}\n")
        f.write(f"Solved: {'yes' if result['solved'] else 'no'}\n")
        f.write(f"Time [s]: {result['time']:.4f}\n")
        f.write(f"Expanded states: {result['num_expanded']}\n")
        f.write(f"Number of actions: {result['num_actions']}\n")

        if result["actions"]:
            f.write("\nAction plan:\n")
            for i, action in enumerate(result["actions"], 1):
                f.write(f"  {i}. {action}\n")

    print(f"Saved: {filepath}")
