import queue
from node import Node
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
        while not frontier.empty() and num_solutions < 10:
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