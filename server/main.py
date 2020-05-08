import os
from flask import Flask
from flask_cors import CORS
port = int(os.environ.get("PORT", 5000))

def create_app(config_filename):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_filename)

    from app import api_bp, template_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(template_bp, url_prefix='/')

    from Model import db
    db.init_app(app)

    return app

app = create_app("config")
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
