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