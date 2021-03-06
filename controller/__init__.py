#!/usr/bin/python

from babel import Locale

from flask import Flask, g, session, request
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect

c3bottles = Flask(__name__,
    static_folder="../static",
    template_folder="../templates"
)

# We need to set this here to prevent the depreciation warning
c3bottles.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

def load_config():
    c3bottles.config.from_object("config")

db = SQLAlchemy(c3bottles, session_options={"autoflush": False})

lm = LoginManager(c3bottles)

bcrypt = Bcrypt(c3bottles)

csrf = CSRFProtect(c3bottles)

babel = Babel(c3bottles)
c3bottles.config["BABEL_TRANSLATION_DIRECTORIES"] = "../translations"

languages = ("en", "de")
locales = {l: Locale(l) for l in languages}
language_list = sorted(
    [l for l in languages],
    key=lambda k: locales[k].get_display_name()
)


def get_locale():
    """
    Get the locale from the session. If no locale is available, set it.
    """
    if "lang" not in session:
        set_locale()
    return session["lang"]


def set_locale():
    """
    Set the locale in the session to one of the available languages.
    If a language has been given via the URL, it is set if it is a valid
    language. If no language has been given via the URL and no language
    is present in the session, the default language will be determined
    according to what the user's browser prefers.
    """
    if "lang" in request.args and request.args["lang"] in language_list:
        session["lang"] = request.args["lang"]
    if "lang" not in session:
        session["lang"] = request.accept_languages.best_match(language_list)
    g.languages, g.locales = language_list, locales


babel.localeselector(get_locale)
c3bottles.before_request(set_locale)

# Trim and strip blocks in jinja2 so no unnecessary
# newlines and tabs appear in the output:
c3bottles.jinja_env.trim_blocks = True
c3bottles.jinja_env.lstrip_blocks = True

from view.api import api
from view.main import index, faq, dp_list, dp_map, dp_view
from view.create import create_dp
from view.edit import edit_dp
from view.report import report
from view.visit import visit
from view.user import login, logout
from view.statistics import stats
c3bottles.register_blueprint(api)
c3bottles.register_blueprint(stats)

# vim: set expandtab ts=4 sw=4:
