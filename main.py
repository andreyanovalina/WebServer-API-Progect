from flask import Flask, render_template, redirect, make_response, request, session, abort, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from flask_restful import abort, Api


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/shop.sqlite")
    app.run()


@app.route("/")
def catalog():
    return render_template("base.html", title='Интернет-магазин книг')


if __name__ == '__main__':
    main()