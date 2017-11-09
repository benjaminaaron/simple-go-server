# Simple Go server using the Go Text Protocol

**_This project is not completed and abandoned for now._**
The meta game logic is (sort of) in place, but there is no actual Go game engine connected though.
Three types of websocket-clients are prototyped: terminal in the browser, python script and telegram bot.
It may serve as architectural inspiration for future Django (Channels) projects of mine.

## Setup

Requires **Python 3.6** or newer.

Navigate to this cloned repository and create a virtual environment:
`python -m venv .venv`. Sometimes it's `python3` instead, check which one is the **3.6+** version on your system by running `python`, leave again with `quit()`.

Activate it using `source activate .venv` on macOS or `.\.venv\Scripts\activate` on windows.

Install the requirements: `pip install -r requirements.txt`.

If you use an IDE like PyCharm, set the newly created `.venv` as Project Interpreter.

Initialise the database: `python manage.py migrate`. 

And whenever you change something regarding the database models (_models.py_) run `python manage.py makemigrations go_server_app` and then `python manage.py migrate` again. This will update the database to reflect your new models.

Add administrators using `python manage.py createsuperuser`.

## Startup

`python manage.py runserver` starts the Django server at `localhost:8000`.

Admin options are located at `/admin`.

## Playing

Just a dummy implementation, no game logic so far.

## Screenshot

![](https://user-images.githubusercontent.com/5141792/32623311-06aa15fa-c586-11e7-8d26-d94789a3fccd.png)
