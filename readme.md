# q-messages

A minimal message board application which I created in order to familiarize myself with Python, Flask and SQLAlchemy.

## Key points

- Authentication via 0auth, using Google Sign in as identity provider.
- Server side rendering via the jinja2 template engine.
- Recursive indentation: any reply can be replied to, to any level (until the styling breaks 🙈).
- SQLAlchemy as database ORM.
- Deployed on Heroku with Gunicorn as WSGI.

## Have a look!

The project is hosted on Heroku:
https://q-messages.herokuapp.com/

## Screenshots

![Screenshot of q-messages web app](https://raw.githubusercontent.com/qvistdev09/q-messages/main/presentation/q-messages.png)