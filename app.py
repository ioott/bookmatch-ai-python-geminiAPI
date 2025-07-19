import os
import google.generativeai as genai
from flask import Flask, render_template, request
from user_data import get_user_history
from logs import save_log
from book_recommendations import (
    recommend_fiction,
    recommend_non_fiction,
    recommend_science,
    recommend_fantasy
)

app = Flask(__name__)

# Configurar a chave de API
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Definir o modelo generativo com as funções disponíveis
magical_if = genai.GenerativeModel(
    "gemini-1.5-flash",
    tools=[
        recommend_fiction,
        recommend_non_fiction,
        recommend_science,
        recommend_fantasy
    ]
)


def ia_decision(user_id, history):
    business_rules = """
    Analise o histórico de compras do usuário e chame diretamente a função
      correspondente à categoria de livros recomendada.

    Regras:
    1. Se o usuário comprou mais livros de ficção, recomende ficção.
    2. Se o usuário comprou mais livros de não ficção, recomende não ficção.
    3. Se o usuário demonstrou interesse em ciência, recomende ciência.
    4. Se o usuário demonstrou interesse em fantasia, recomende fantasia.
    5. Caso contrário, ofereça uma recomendação geral de ficção.

    ATENÇÃO: Sempre retorne a resposta da função chamada.
    Não explique, apenas chame.
    """
    user_decision = magical_if.start_chat(
        enable_automatic_function_calling=True
    )

    message = (
        f"Histórico do usuário {user_id}: {history}\n"
        f"Regras de negócio:\n{business_rules}"
    )

    response = user_decision.send_message(message)

    # Tenta obter a chamada de função feita pela IA
    try:
        function_call = response.candidates[0].content.parts[0].function_call
        function_name = function_call.name

        user_function = {
            "recommend_fiction": recommend_fiction,
            "recommend_non_fiction": recommend_non_fiction,
            "recommend_science": recommend_science,
            "recommend_fantasy": recommend_fantasy
        }.get(function_name)

        if user_function:
            return user_function(user_id)
    except (AttributeError, IndexError):
        pass

    # Caso nenhuma função tenha sido chamada, retorna o texto
    return response.text


@app.route('/recommend/<int:user_id>')
def recommend(user_id):
    history = get_user_history(user_id)
    if not history:
        return "Usuário não encontrado", 404
    ia_response = ia_decision(user_id, history)
    save_log(user_id, history, ia_response)
    return render_template(
        'recommendation.html',
        user_id=user_id,
        message=ia_response
    )


@app.route('/chat/<int:user_id>', methods=['GET', 'POST'])
def chat(user_id):
    history = get_user_history(user_id)
    if not history:
        return "Usuário não encontrado", 404

    response = None

    if request.method == 'POST':
        question = request.form.get('question')
        user_decision = magical_if.start_chat(
            enable_automatic_function_calling=True
        )
        gemini_response = user_decision.send_message(
            f"Usuário {user_id}, histórico: {history}. Pergunta: {question}"
        )

        try:
            function_call = (
                gemini_response
                .candidates[0]
                .content.parts[0]
                .function_call
            )
            function_name = function_call.name
            user_function = {
                "recommend_fiction": recommend_fiction,
                "recommend_non_fiction": recommend_non_fiction,
                "recommend_science": recommend_science,
                "recommend_fantasy": recommend_fantasy
            }.get(function_name)

            if user_function:
                response = user_function(user_id)
            else:
                response = gemini_response.text
        except (AttributeError, IndexError):
            response = gemini_response.text

        save_log(user_id, history, response)

    return render_template('chat.html', user_id=user_id, response=response)


@app.route('/perfil/<int:user_id>', methods=['GET', 'POST'])
def perfil(user_id):
    history = get_user_history(user_id)
    if not history:
        return "Usuário não encontrado", 404

    if request.method == 'POST':
        name = request.form.get('name')
        preferences = request.form.getlist('preferences')
        # aqui vamos salvar nome e preferências
        history['name'] = name
        history['preferences'] = preferences

    return render_template('perfil.html', user_id=user_id, history=history)


if __name__ == '__main__':
    app.run(debug=True)
