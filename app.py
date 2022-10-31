from datetime import datetime

import flask_talisman
import config
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, render_template, session, url_for, request
from db import Session
from message import Message
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from flask_talisman import Talisman

config.load()

app = Flask(__name__)
if env.get("PYTHON_ENV") == "production":
    csp = dict(flask_talisman.GOOGLE_CSP_POLICY)
    csp["default-src"] = ['\'self\'', 'kit.fontawesome.com', 'ka-f.fontawesome.com']
    csp["script-src"] = ['\'self\'', 'kit.fontawesome.com']
    csp["style-src"] = ['\'self\'', '\'unsafe-inline\'']
    Talisman(app, content_security_policy=csp)
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
    try:
        dbSession = Session()
        messages = dbSession.query(Message).options(joinedload(Message.children)).filter(Message.parent_message.is_(None)).order_by(
            desc(Message.created_at)).all()
        template_output = render_template(
            "home.html", session=session.get('user'), messages=messages)
        dbSession.close()
        return template_output
    except:
        return redirect(url_for('error'))


@app.route("/new-post")
def new_post():
    userSession = session.get('user')
    if userSession is None:
        return redirect("/")
    return render_template("new-post.html", session=session.get('user'))


@app.route("/new-post", methods=["POST"])
def handle_post_request():
    try:
        messageBody = request.form.getlist("body")[0]
        userSession = session.get('user')
        if len(messageBody) > 5000 or userSession is None:
            return redirect(url_for('error'))
        nickname = userSession.get("userinfo").get("nickname")
        sub = userSession.get("userinfo").get("sub")
        dbSession = Session()
        newMessage = Message(messageBody, nickname, sub, datetime.now())
        dbSession.add(newMessage)
        dbSession.commit()
        dbSession.close()
        return redirect('/')
    except:
        return redirect(url_for('error'))


@app.route('/messages/<int:post_id>/reply')
def serve_reply_form(post_id):
    userSession = session.get('user')
    if userSession is None:
        return redirect(url_for('error'))
    dbSession = Session()
    message = dbSession.query(Message).filter(
        Message.id == post_id).one_or_none()
    dbSession.close()
    if message is None:
        return redirect(url_for('error'))
    return render_template("reply-form.html", session=session.get('user'), message=message)


@app.route('/messages/<int:post_id>/reply', methods=["POST"])
def handle_reply(post_id):
    try:
        userSession = session.get('user')
        if userSession is None:
            return redirect(url_for('error'))
        dbSession = Session()
        message = dbSession.query(Message).filter(
            Message.id == post_id).one_or_none()
        if message is None:
            return redirect(url_for('error'))
        messageBody = request.form.getlist("body")[0]
        if len(messageBody) > 5000:
            return redirect(url_for('error'))
        nickname = userSession.get("userinfo").get("nickname")
        sub = userSession.get("userinfo").get("sub")
        reply = Message(messageBody, nickname, sub, datetime.now())
        reply.parent_message = message.id
        dbSession.add(reply)
        dbSession.commit()
        dbSession.close()
        return redirect('/')
    except:
        return redirect(url_for('error'))


@app.route("/error")
def error():
    return render_template("error.html", session=session.get('user'))
