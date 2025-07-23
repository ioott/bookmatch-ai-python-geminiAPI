import re
from flask import Blueprint, render_template, request
from services.genai_service import configure_genai
from logs import get_user_history, save_log

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/chat/<int:user_id>', methods=['GET', 'POST'])
def chat(user_id):
    """
    Rota para interação do usuário com a IA.
    """
    history = get_user_history(user_id)

    if not history:
        return render_template('error_redirect.html')

    response = None

    if request.method == 'POST':
        question = request.form.get('question')

        try:
            model = configure_genai()
            session = model.start_chat(enable_automatic_function_calling=True)

            prompt = (
                f"Você é uma especialista em livros e pode conversar "
                f"livremente sobre obras literárias, personagens, enredos, "
                f"gêneros e autores. O nome do usuário é "
                f"{history.get('name', f'Usuário {user_id}')}. "
                f"As preferências dele são: "
                f"{', '.join(history.get('preferences', [])) or 'nenhuma'}. "
                f"Histórico: {history}. "
                f"Pergunta: {question}. Responda na mesma língua da pergunta,"
                f" com até 500 caracteres."
                f"Fale diretamente com o usuário."
            )

            gemini_response = session.send_message(prompt)
            response = gemini_response.text

            save_log(user_id, history, response)

        except Exception as e:
            print(f"Erro ao usar a IA: {e}")
            response = "⚠️ A IA está indisponível, retorne em 24h."

    formatted_response = None
    if response:
        formatted_response = response.replace('\n', '<br>')
        formatted_response = re.sub(
            r'(?<=<br>)\s*(Ficção|Não[- ]Ficção|Ciência|Fantasia)\s*:(?=<br>)',
            r'<b>\1:</b>',
            f"<br>{formatted_response}<br>"
        )[4:-4]
        formatted_response = formatted_response.replace('**', '')
        formatted_response = formatted_response.replace('* ', '• ')

    return render_template(
        'chat.html',
        user_id=user_id,
        response=formatted_response,
        history=history
    )
