from flask import Flask, request
from flask_session import Session
#from src.parse_data import save_text_to_pcd
import subprocess
import json



#app = Flask(__name__)

'''
[x] Make sure .so bui   lds correctly
[x] Call .so file from python
[x] Receive point cloud data in the form of PCD
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
        self.run(options.get('host', "0.0.0.0"), options.get('port', 8081), options, use_reloader=False)


app = WebApplication("spatial_computing_lab")
app.listen(port=8081)



@app.route('/')
def index():
    print('hello world')
    #json.
    return 'Index page'


@app.route('/stl', methods=['POST', 'GET'])
def stl():
    scene_mesh_text = request.get_data().decode()
    save_text_to_pcd(scene_mesh_text)

    print('Scene mesh received and saved successfully!')

    process = subprocess.Popen(['./src/CorrespondenceGrouping', 'src/mesh_folder/scene_mesh.pcd', 'src/mesh_folder/scene_mesh.pcd'],
                               stdout=subprocess.PIPE)
    out = process.stdout.read().decode()

    print(out)

    return out


if __name__ == "__main__":
    app = WebApplication("spatial_computing_lab")
    app.listen(port=8081)
