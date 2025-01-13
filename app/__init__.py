from flask import Flask

def create_app():
    # In your Flask app
    app = Flask(__name__)
    app.static_folder = 'static'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.secret_key = 'your_secret_key'

    from app.routes import bp
    app.register_blueprint(bp)

    return app
