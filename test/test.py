from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")  # Ensure templates folder
CORS(app)

@app.route('/')
def home():
    return render_template('test.html')  # Ensure test.html is inside 'templates/'

@app.route('/api/data', methods=['GET'])
def api_data():
    data = {'result': 5}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
