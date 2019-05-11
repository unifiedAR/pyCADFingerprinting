from flask import Flask, request
from flask_session import Session


app = Flask(__name__)


'''
[ ] Make sure .so builds correctly
[ ] Call .so file from python

[ ] Receive point cloud data in the form of PCD

[ ] Return transform in the form of a matrix/quaternion

'''


class WebApplication(Flask):
    """
    A wrapper for a Flask application to simplify app configuration and launching.
    """

    def __init__(self, app_name=None, debug=False):
        # Call __init__ from the Flask superclass
        super().__init__(app_name or __name__)

        # Set configuration variables
        self.debug = debug
        Session(self)  # for the cookies

    def listen(self, **options):
        """ Asks Flask to begin listening to HTTP requests, with options if given. """
        self.run(options.get('host', "0.0.0.0"), options.get('port', 3000), options, use_reloader=False)


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





if __name__ == "__main__":
    app = WebApplication("spatial_computing_lab")
app.listen(port=8080)