from flask import Blueprint, render_template, request, redirect
from logs import get_user_history
from constants.genres import GENRES

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/perfil/<int:user_id>', methods=['GET', 'POST'])
def perfil(user_id):
    """
    Rota para visualizar e atualizar nome e preferências do perfil.
    """
    history = get_user_history(user_id)

    if not history:
        return '''
            <html>
            <head>
                <meta http-equiv="refresh" content="2;url=/" />
            </head>
            <body>
                <h2>Ops, algo deu errado por aqui.</h2>
                <p>Vou te levar de volta para a página inicial.</p>
            </body>
            </html>
        '''

    if request.method == 'POST':
        name = request.form.get('name')
        preferences = request.form.getlist('preferences')

        history['name'] = name
        history['preferences'] = preferences

        return redirect(f'/chat/{user_id}')

    return render_template(
        'profile.html',
        user_id=user_id,
        history=history,
        genres=GENRES
    )
