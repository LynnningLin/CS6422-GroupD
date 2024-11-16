# **When you're running the flask script, make sure to run it from the project folder, not inside the frontend folder**.
* The Flaskenv file is outside the frontend folder
* Running Flask App
    * Go to project root
    * type into terminal 
    ```py
    python3 -m flask run
    <!-- Or whatever version of Python you are running -->
    ```

* **I Used an absolute import for app.py to be able to call the simulation function() inside basic_test.py**
    * used from backend.basic_test import simulation
    * from backend.ANSI import Colours --> (Note that I diabled all ANSI prints in the basic_test.py for testing as app.py was having difficulties actually importing ANSI)
<hr>

### .Flaskenv
* i took the .flaskenv file out into the project root and then redirected the to this (FLASK_APP=frontend.app:app)
* (frontend.app:app) means:
    * frontend.app is the path to the module (app.py inside the frontend folder).
    * app after the colon(:app) refers to the Flask application instance defined inside that module
        * If you go to app.py, you'll see app = Flask(__name__)  at the top of the script, this is the instance I'm talking about
    * I also created an __init__.py empty file in the frontend foldder, adding this file makes the frontend folder to be treated a python package, This tells the interpreter that this package contains CODE to INITIALISE the flask app
    * this is useful when the project is becoming more and more complex, if it's a simple project then having 1 app.py file is okay but with our use of multiple scripts, this will help with scalability

<hr>

* Also i couldnt import ANSI and the basic_test has many dependencies on ANSI so i did a try/except just so the ansi package would be isolated from the flask app as flask doesnt actually need ansi to run
* UPDATE --> I actually disiabled ANSI all together just for the sake of testing flask with the simulation
<hr>

## UPDATE FOR FRONTEND/BACKEND INTERGRATION
* I had to comment out a lot of the environment and the declared instances code at the end as well as the user input and the threading in basic_test.py.
* I had to take the simulation out of the function as well so it was easier for me to access the classes in the flask app
* I re-declared all of them in the flask app instead and got access to the hvac instance and confidgured the temps shown in the frontend to where they now actually show real data. 
* Little tid-bit but i changed the size of the temerature text in the frontend because they were overlapping onto the icons 