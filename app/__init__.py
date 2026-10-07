import os
from flask import Flask
from dotenv import load_dotenv
from .routes import site

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-this-secret-key")
    app.context_processor(lambda: {"MODULE_LABELS": {
        "rooms":"Rooms","facilities":"Facilities","gallery":"Gallery",
        "testimonials":"Testimonials","faqs":"FAQs"
    }})
    app.register_blueprint(site)
    return app
