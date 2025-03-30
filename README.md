# Qanit: The Intelligent Quran Verses Selector

## Overview
This project implements a search-based solver for the **Qanit Problem** using various search algorithms, particularly **A* Search**. It models the problem as a graph search, where nodes represent states, and edges represent transitions between states with associated costs. The objective is to find an optimal path from an initial state to a goal state.

## Features
- **General Search Algorithm**: A flexible implementation supporting different search strategies.
- **A* Search Implementation**: Uses both cost (`g`) and heuristic (`h`) values for optimal pathfinding.
- **State Representation with Node Class**: Encapsulates states, parents, costs, and solution path tracking.
- **Frontier Management with Priority Queue**: Ensures efficient node expansion.
- **Test Suite**: A function to validate different search strategies on the Qanit problem.

## Installation
Ensure you have Python installed. Clone the repository and navigate to the project folder.
```sh
$ git clone <repository_url>
$ cd qanit-problem-solver
```

## Usage
To run the A* search on the Qanit problem, execute:
```sh
$ python main.py
```

## Code Explanation
### **1. Node Class** (`node.py`)
The `Node` class represents a search tree node with:
- `state`: The current state
- `parent`: Reference to the parent node
- `action`: The action taken to reach this node
- `g`: Cost from the start node
- `f`: Total evaluation cost (`g + h`)
- `get_solution_path()`: Retrieves the sequence of actions leading to the goal

### **2. General Search** (`search.py`)
The `GeneralSearch` class implements a flexible search framework:
- `set_frontier()`: Initializes the frontier based on the search strategy
- `search()`: Performs the search using A*

### **3. Qanit Problem Definition** (`qanit_problem.py`)
Defines the problem, including:
- Initial and goal states
- State transition model
- `expand_node()`: Generates successors based on valid transitions

## Example Output
```sh
------------------------------------A* Search------------------------------------
Current Node: (state info...)
Goal reached: 100
Solution Path (A* Search): [...]
Actual Path Cost (A* Search): 12
Total Evaluation Cost (A* Search): 18
```

## Troubleshooting
- **Unhashable Type: List Error**: Ensure `Node.__hash__` converts lists to tuples.
- **Algorithm Not Expanding Nodes**: Verify `expand_node()` correctly generates successors.
- **Infinite Loop / No Solution**: Check the problem definition and heuristic function.

## Future Improvements
- Implement additional search strategies (e.g., BFS, UCS, Greedy Best-First)
- Optimize heuristic functions for better performance
- Add visualization of the search process

## License
This project is open-source under the MIT License.

