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


# ── Subgoal decomposition ──────────────────────────────────

def apply_actions_to_state(domain, state, action_names):
    """Apply a sequence of actions (by name) to a state and return the resulting state."""
    current = dict(state)
    action_map = {act.name: act for act in domain.actions}
    for name in action_names:
        act = action_map[name]
        current.update(act.effects)
    return current


def solve_with_subgoals(domain, initial_state, subgoals, final_goal,
                        heur=None, timeout_seconds=300):
    """Solve a planning problem by decomposing it into sequential subgoals.

    Instead of solving the full problem at once, we solve a chain:
      initial → subgoal_1 → subgoal_2 → ... → final_goal
    Each sub-problem starts from the state produced by the previous one.
    """
    from aipython.stripsProblem import Planning_problem

    current_state = dict(initial_state)
    all_actions = []
    total_time = 0
    total_expanded = 0
    subgoal_details = []

    goals = subgoals + [final_goal]
    goal_names = [f"Subgoal {i+1}" for i in range(len(subgoals))] + ["Final goal"]

    for goal, name in zip(goals, goal_names):
        problem = Planning_problem(domain, current_state, goal)
        result = solve(problem, heur=heur, timeout_seconds=timeout_seconds)

        subgoal_details.append({"name": name, "goal": goal, "result": result})

        if not result["solved"]:
            return {
                "solved": False,
                "time": total_time + result["time"],
                "actions": all_actions,
                "num_actions": len(all_actions),
                "num_expanded": total_expanded + result["num_expanded"],
                "subgoal_details": subgoal_details,
            }

        all_actions.extend(result["actions"])
        total_time += result["time"]
        total_expanded += result["num_expanded"]
        current_state = apply_actions_to_state(domain, current_state, result["actions"])

    return {
        "solved": True,
        "time": total_time,
        "actions": all_actions,
        "num_actions": len(all_actions),
        "num_expanded": total_expanded,
        "subgoal_details": subgoal_details,
    }


def solve_and_record_subgoals(domain, initial_state, subgoals, final_goal,
                              problem_name, experiment_name,
                              heur=None, timeout_seconds=300):
    print(f"\n{'='*60}")
    print(f"Experiment: {experiment_name}")
    print(f"Problem: {problem_name}")
    heur_label = heur.__name__ if heur else "none"
    print(f"Heuristic: {heur_label}")
    print(f"Subgoals: {len(subgoals)}")
    print(f"{'='*60}")

    result = solve_with_subgoals(domain, initial_state, subgoals, final_goal,
                                 heur=heur, timeout_seconds=timeout_seconds)

    for detail in result["subgoal_details"]:
        sub = detail["result"]
        status = "solved" if sub["solved"] else "FAILED"
        print(f"  {detail['name']}: {status} in {sub['time']:.4f}s, "
              f"{sub['num_expanded']} expanded, {sub['num_actions']} actions")

    print(f"\n--- Overall ---")
    if result["solved"]:
        print(f"Solution found in {result['time']:.4f}s")
        print(f"Total actions: {result['num_actions']}")
        print(f"Total expanded states: {result['num_expanded']}")
        print("Action plan:")
        for i, action in enumerate(result["actions"], 1):
            print(f"  {i}. {action}")
    else:
        print(f"No solution found (timeout or subgoal failure)")
        print(f"Total expanded states: {result['num_expanded']}")

    _save_subgoal_result(experiment_name, problem_name, heur_label, subgoals, result)
    return result


def _save_subgoal_result(experiment_name, problem_name, heur_label, subgoals, result):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{experiment_name}_{heur_label}_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Experiment: {experiment_name}\n")
        f.write(f"Problem: {problem_name}\n")
        f.write(f"Heuristic: {heur_label}\n")
        f.write(f"Subgoals: {len(subgoals)}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*50}\n")

        for detail in result["subgoal_details"]:
            sub = detail["result"]
            f.write(f"\n{detail['name']}:\n")
            f.write(f"  Goal: {detail['goal']}\n")
            f.write(f"  Solved: {'yes' if sub['solved'] else 'no'}\n")
            f.write(f"  Time [s]: {sub['time']:.4f}\n")
            f.write(f"  Expanded states: {sub['num_expanded']}\n")
            f.write(f"  Actions: {sub['num_actions']}\n")
            if sub["actions"]:
                for j, action in enumerate(sub["actions"], 1):
                    f.write(f"    {j}. {action}\n")

        f.write(f"\n{'='*50}\n")
        f.write(f"Overall:\n")
        f.write(f"  Solved: {'yes' if result['solved'] else 'no'}\n")
        f.write(f"  Total time [s]: {result['time']:.4f}\n")
        f.write(f"  Total expanded states: {result['num_expanded']}\n")
        f.write(f"  Total actions: {result['num_actions']}\n")

        if result["actions"]:
            f.write("\nComplete action plan:\n")
            for i, action in enumerate(result["actions"], 1):
                f.write(f"  {i}. {action}\n")

    print(f"Saved: {filepath}")
