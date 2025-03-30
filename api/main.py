import csv
import time
import os
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from node import Node
from problem import QanitProblem
from general_search import GeneralSearch

# flask app setup
app = Flask(__name__, template_folder="templates")  # Ensure templates folder
CORS(app)
@app.route('/')
def home():
    return render_template('index.html')  # Ensure test.html is inside 'templates/'

@app.route('/api/data', methods=['POST'])
def api_data():
    verse_count = request.json.get('verseCount', 100)  # Default to 100 if not provided
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
    state_transition_model = {int(row[0]): (int(row[3]), int(row[4]), row[1]) for row in data}
    initial_state = (0, 0, [])  
    goal_state = verse_count  
    qanit_problem = QanitProblem(initial_state, goal_state, state_transition_model)
    timestamp = time.time()
    seq = test_strategy(qanit_problem, "A*", "A* Search")  
    elapsed_time = time.time() - timestamp
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print("Final sequence of chapters is: ", seq)

    return jsonify(seq)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get Render's assigned port
    app.run(host='0.0.0.0', port=port, debug=True)
