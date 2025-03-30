import csv
import time
import queue


# ------------------------------
# 1. Node Class Definition
# ------------------------------
class Node:
    def __init__(self, state, parent=None, action=None, g=0, f=0):
        """
        Initialize a search tree node.

        Input Parameters:
            - state: The state represented by this node
            - parent: The parent Node that generated this node. Default is None.
            - action: The action taken to reach this node from the parent. Often the same as the state.
            - g: The cumulative cost (actual cost) from the start node to this node. Default is 0.
            - f: The evaluation function value for the node (e.g., for UCS, A*). Default is 0.

        Output:
            - A Node instance with attributes: state, parent, action, g, f, and depth.

        """
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g  # Cumulative cost from start to this node
        self.f = f  # Evaluation cost (g + heuristic if applicable)
        # Calculate the depth of the node
        if parent is None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1

    def __hash__(self):
        """
        Compute a hash value for the node.

        Input Parameters:
            - None (uses the node's state)

        Output:
            - An integer hash value.
        """

        return hash(self.state)

    def __eq__(self, other):
        """
        Check equality with another Node based on the state.

        Input Parameters:
            - other: Another Node instance.

        Output:
            - True if the states are equal, False otherwise.
        """
        return isinstance(other, Node) and self.state == other.state

    def __gt__(self, other):
        """
        Compare this node with another node based on the evaluation function (f).

        Input Parameters:
            - other: Another Node instance.

        Output:
            - True if this node's f is greater than the other's f, else False.
        """
        return isinstance(other, Node) and self.f > other.f
    
    def get_solution_path(self):
        """
        Traces back the path from this node to the root.

        Returns:
        - List of chapters that were selected.
        """
        path = []
        node = self
        while node:
            if node.action is not None:  # Ignore the root node
                path.append(node.action)
            node = node.parent
        return list(reversed(path))  # Reverse to get correct order
class QanitProblem:
    def __init__(self, initial_state, goal_state, state_transition_model, tolerance=5):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.state_transition_model = state_transition_model
        self.tolerance = tolerance
    
    def is_goal(self, current_state):
        verses_count = current_state[0]
        return verses_count >= self.goal_state and verses_count <= self.goal_state + self.tolerance
    
    def get_valid_actions(self, current_state):
        _, _, selected_chapters = current_state
        return [ch for ch in self.state_transition_model if ch not in selected_chapters]
    
    def expand_node(self, node, use_cost=True, use_heuristic=False):
        state = node.state
        valid_actions = self.get_valid_actions(state)
        
        child_nodes = []
        for chapter in valid_actions:
            num_verses, num_words, _ = self.state_transition_model[chapter]
            new_state = (state[0] + num_verses, state[1] + num_words, state[2] + [chapter])
            if new_state[0] > self.goal_state + 2*self.tolerance:
                continue  # Skip this chapter as it would take us too far past the goal
            g = node.g + num_verses
            h = self.heuristic(new_state) if use_heuristic else 0
            f = g + h
            child_nodes.append(Node(new_state, parent=node, action=chapter, g=g, f=f))
        return child_nodes
    
    def get_total_cost(self, g, state, use_heuristic=True, use_cost=True):
        h = self.heuristic(state)
        total = 0
        if use_cost:
            total += g
        if use_heuristic:
            total += h
        return total
    
    def heuristic(self, state):
        # If we've exceeded the goal, penalize proportionally
        if state[0] > self.goal_state:
            return (state[0] - self.goal_state) * 2
        return max(0, self.goal_state - state[0])
    
    def print_node(self, node):
        print("Action:", node.action, "| Depth:", node.depth)
class GeneralSearch:
    def __init__(self, problem):
        self.problem = problem
        self.use_cost = True
        self.use_heuristic = False

    def set_frontier(self, search_strategy="A*"):
        if search_strategy == "A*":
            frontier = queue.PriorityQueue()
            self.use_cost = True
            self.use_heuristic = True
        else:
            raise ValueError("Unsupported search strategy: " + str(search_strategy))
        return frontier


    def search(self, search_strategy="A*", max_depth=float('inf')):
        frontier = self.set_frontier(search_strategy)
        explored = set()
        initial_node = Node(self.problem.initial_state)
        frontier.put((initial_node.f, initial_node))
        solutions = []
        num_solutions = 0 #a cutoff to limit the number of solutions found
        while not frontier.empty() and num_solutions < 50:
            _, node = frontier.get()
            self.problem.print_node(node)
            
            if self.problem.is_goal(node.state):
                print("Goal reached:", node.state)
                solutions.append(node)
                num_solutions += 1
                continue

            if node.depth > max_depth:
                continue

            # Convert the list part of the state to a tuple before adding to explored
            hashable_state = (node.state[0], node.state[1], tuple(node.state[2]))
            explored.add(hashable_state)

            for child in self.problem.expand_node(node, self.use_cost, self.use_heuristic):
                # Convert the child state to hashable form for comparison
                child_hashable = (child.state[0], child.state[1], tuple(child.state[2]))
                if child_hashable in explored:
                    continue

                frontier.put((child.f, child))
        if solutions:
            print(f"Found {len(solutions)} solutions.")
            for i, solution in enumerate(solutions):
                print(f"Solution {i+1}: {solution.get_solution_path()}")
                print(f"Needed words: {solution.state[1]}, Verses: {solution.state[0]}")
            
            # First sort by how close the verse count is to the goal, then by word count
            sol = min(solutions, key=lambda x: (abs(x.state[0] - self.problem.goal_state), x.state[1]))
            
            print(f"Most optimal solution: {sol.state}")
            sequence = []
            for i in sol.state[2]:
                sequence.append(self.problem.state_transition_model[i][2])
            return (sol, sequence)
        else:
            return None


# data setup
file_path = "./data/quran_chapters.csv"

with open(file_path, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    data = [row for row in reader]

data.pop(0)  # Remove header


# Test function implementation


def test_strategy(problem, strategy, description, max_depth=float('inf')):
    print(f"-------------------- {description} --------------------")

    search_instance = GeneralSearch(problem)
    solution_node, sequence = search_instance.search(search_strategy=strategy, max_depth=max_depth)

    if solution_node:
        path = solution_node.get_solution_path()
        print(f"Solution Path: {path}")
        print(f"Actual Path Cost: {solution_node.g}")
        print(f"Total Evaluation Cost: {solution_node.f}")
        return sequence
    else:
        print(f"No solution found for {description}!")
        return None
# Ensure `data` is defined before using it
if __name__ == "__main__":
    state_transition_model = {int(row[0]): (int(row[3]), int(row[4]), row[1]) for row in data}
    initial_state = (0, 0, [])  
    goal_state = 20
    qanit_problem = QanitProblem(initial_state, goal_state, state_transition_model)
    timestamp = time.time()
    seq = test_strategy(qanit_problem, "A*", "A* Search")  
    elapsed_time = time.time() - timestamp
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print("Final sequence of chapters is: ", seq)



def test_QanitProblem_class(num_verses=100):
    toy_state_transition_model = {int(row[0]): (int(row[3]), int(row[4])) for row in data}
    print("State Transition Model:", toy_state_transition_model)
    initial_state = (0, 0, []) # (num_verses, num_words, selected_chapters)
    goal_state = num_verses
    toy_problem = QanitProblem(initial_state, goal_state, toy_state_transition_model)

    test_state = (100, 200, [1, 2])
    print("Test is_goal:", toy_problem.is_goal(test_state))
    print("Valid actions:", toy_problem.get_valid_actions(test_state))

    test_node = Node(test_state)
    expanded_nodes = toy_problem.expand_node(test_node, use_heuristic=True)
    print("Expanded Nodes:", [node.state for node in expanded_nodes])

    total_cost = toy_problem.get_total_cost(100, test_state)
    print("Total Cost:", total_cost)

    for node in expanded_nodes:
        toy_problem.print_node(node)
    if expanded_nodes:
        solution_path = expanded_nodes[0].get_solution_path()
        print("Solution Path:", solution_path)


