from flask import Flask
from routes.home import home_bp
from routes.chat import chat_bp
from routes.profile import profile_bp


def create_app():
    """Cria e configura uma instância da aplicação Flask."""
    app = Flask(__name__)
    app.register_blueprint(home_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(profile_bp)
    return app


# Cria a instância do app para que o Hugging Face possa encontrá-la
app = create_app()

# O bloco abaixo é mantido para permitir a execução local
if __name__ == '__main__':
    app.run(debug=True)