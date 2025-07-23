from flask import Blueprint, render_template, request, redirect
from time import time
from logs import save_log, get_all_users
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

        new_id = int(time())

        initial_history = {
            'name': name,
            'preferences': preferences,
            'chat': []
        }

        save_log(
            user_id=new_id,
            history=initial_history,
            response="Perfil criado."
        )

        return redirect(f'/chat/{new_id}')

    return render_template(
        'start.html',
        profiles=get_all_users(),
        genres=GENRES
    )
