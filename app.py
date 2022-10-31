import config
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, render_template, session, url_for, request
from db import Session
from message import Message
from sqlalchemy import desc

config.load()

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

auth = OAuth(app)

auth.register("auth0",
              client_id=env.get("AUTH0_CLIENT_ID"),
              client_secret=env.get("AUTH0_CLIENT_SECRET"),
              client_kwargs={"scope": "openid profile email"},
              server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
              )


@app.route("/login")
def login():
    return auth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = auth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


@app.route("/")
def home():
    dbSession = Session()
    messages = dbSession.query(Message).filter(Message.parent_message.is_(None)).order_by(
        desc(Message.created_at)).all()
    template_output = render_template(
        "home.html", session=session.get('user'), messages=messages)
    dbSession.close()
    return template_output


@app.route("/new-post")
def new_post():
    return render_template("new-post.html", session=session.get('user'))


@app.route("/new-post", methods=["POST"])
def handle_post_request():
    try:
        messageBody = request.form.getlist("body")[0]
        if len(messageBody) > 255:
            return redirect(url_for('error'))
        return "HELLO"
    except:
        return redirect(url_for('error'))


@app.route("/error")
def error():
    return "there was an error"
