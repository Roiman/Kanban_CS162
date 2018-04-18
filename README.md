Welcome to the world of Kanban!

The app is far from complete, but shows many functions learnt in CS162, such as logging in, using @routes, rendering HTML, and at least conceptually – unit testing.

The HTML files include some 'dirty' elements, mostly of functionalities that did not get fully developed (such as "drag-and-drop" for task allocation), and the testing file only includes the list of test that should be written – due to technical difficulties, they did not get written. A better programmer would have worked with TDD, but much of my work was focused on understanding how things work – this is the first app I ever written.

after installing your local virtual environment (`python3.6 -m venv .venv` would work) and activating it (`source .venv/bin/activate`), you can use `pip3 install -r requirements.txt` to install all the dependencies required for written this local kanban board, and run it with `python3 app.py`

you can create users freely, but will only see your own user's tasks. To check out some of the many things this app is currently lacking, please log in with my username: roiman, and the original password: roiman.


to discover the unit tests, run `python3 -m unittest discover test` from the Kanban_app directory. There are 20 tests in planning, only the first one works as desired.