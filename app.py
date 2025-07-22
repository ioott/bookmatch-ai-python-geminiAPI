from flask import Flask
from routes.home import home_bp
from routes.chat import chat_bp
from routes.profile import profile_bp

app = Flask(__name__)

app.register_blueprint(home_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(profile_bp)

if __name__ == '__main__':
    app.run(debug=True)
