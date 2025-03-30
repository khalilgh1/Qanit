from node import Node
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