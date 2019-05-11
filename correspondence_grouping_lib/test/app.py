from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index page'

@app.route('/stl', methods=['POST', 'GET'])
def stl():
    stl_data = request.get_data().decode()
    print(stl_data)
    return 'none'

@app.route('/matrix', methods=['POST', 'GET'])
def matrix():
    matrix_data = request.get_data().decode()
    print(matrix_data)
    return 'none'
