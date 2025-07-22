from flask import Blueprint, render_template, request, redirect
from logs import get_user_history
from constants.genres import GENRES

home_bp = Blueprint('home', __name__)


@home_bp.route('/', methods=['GET', 'POST'])
def inicio():
    """
    Rota inicial para criação de perfil ou acesso a perfis existentes.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        preferences = request.form.getlist('preferences')

        # Simula criação de novo ID com base no maior já existente
        new_id = max(get_user_history.keys(), default=0) + 1

        get_user_history[new_id] = {
            'name': name,
            'preferences': preferences
        }

        return redirect(f'/chat/{new_id}')

    return render_template(
        'start.html',
        profiles=get_user_history,
        genres=GENRES
    )
