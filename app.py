import os
import re
import google.generativeai as genai
from flask import Flask, redirect, render_template, request
from user_data import get_user_history
from logs import save_log

app = Flask(__name__)


# Função para configurar a chave de API
def genai_configuration():
    try:
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

        # Testa se a chave principal está disponível
        test_model = genai.GenerativeModel("gemini-1.5-flash")
        test_model.start_chat().send_message("ping")

        return

    except Exception:
        print("⚠️  Falha com a chave principal, tentando chave reserva 1.")

        try:
            genai.configure(api_key=os.environ['GOOGLE_API_KEY_2'])

            # Testa se a chave reserva 1 está disponível
            test_model = genai.GenerativeModel("gemini-1.5-flash")
            test_model.start_chat().send_message("ping")

            return

        except Exception:
            print("⚠️  Falha com a chave reserva 1, tentando chave reserva 2.")

            try:
                genai.configure(api_key=os.environ['GOOGLE_API_KEY_3'])

                # Testa se a chave reserva 2 está disponível
                test_model = genai.GenerativeModel("gemini-1.5-flash")
                test_model.start_chat().send_message("ping")

                return
            
            except Exception:
                print("❌ Todas as chaves falharam.")


genai_configuration()

# Definir o modelo generativo com as funções disponíveis
magical_if = genai.GenerativeModel("gemini-1.5-flash")


def ia_decision(user_id, history):
    business_rules = """
    Analise o histórico de compras do usuário e recomende livros a ele.

    Regras:
    1. Se o usuário demonstrou interesse em ficção, recomende ficção.
    2. Se o usuário demonstrou interesse em não ficção, recomende não-ficção.
    3. Se o usuário demonstrou interesse em ciência, recomende ciência.
    4. Se o usuário demonstrou interesse em fantasia, recomende fantasia.
    5. Se o usuário não demonstrou interesse em nenhuma categoria, recomende
      os livros mais vendidos no último mês.
    """

    user_decision = magical_if.start_chat(
        enable_automatic_function_calling=True
    )

    message = (
        f"Histórico do usuário {user_id}: {history}\n"
        f"Regras de negócio:\n{business_rules}"
    )

    response = user_decision.send_message(message)

    return response.text


@app.route('/', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        name = request.form.get('name')
        preferences = request.form.getlist('preferences')

        # Simula criação de novo ID
        from user_data import user_histories
        new_id = max(user_histories.keys()) + 1
        user_histories[new_id] = {
            'fiction': 0,
            'non_fiction': 0,
            'science': 0,
            'fantasy': 0,
            'name': name,
            'preferences': preferences
        }

        return redirect(f'/chat/{new_id}')

    return render_template('start.html')


@app.route('/perfil/<int:user_id>', methods=['GET', 'POST'])
def perfil(user_id):
    history = get_user_history(user_id)

    if not history:
        return '''
            <html>
            <head>
                <meta http-equiv="refresh" content="2;url=/">
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

        # aqui vamos salvar nome e preferências
        history['name'] = name
        history['preferences'] = preferences

    return render_template('profile.html', user_id=user_id, history=history)


@app.route('/chat/<int:user_id>', methods=['GET', 'POST'])
def chat(user_id):
    history = get_user_history(user_id)

    if not history:
        return '''
            <html>
            <head>
                <meta http-equiv="refresh" content="2;url=/">
            </head>
            <body>
                <h2>Ops, algo deu errado por aqui.</h2>
                <p>Vou te levar de volta para a página inicial.</p>
            </body>
            </html>
        '''

    response = None

    if request.method == 'POST':
        question = request.form.get('question')

        user_decision = magical_if.start_chat(
            enable_automatic_function_calling=True
        )

        name = history.get("name", f"Usuário {user_id}")
        preferences = history.get("preferences", [])

        prompt = (
            f"Você é uma especialista em livros e pode conversar livremente "
            f"sobre obras literárias, personagens, enredos, gêneros e autores."
            f" O nome do usuário é {name} e seu ID é {user_id}. A informação "
            f"sobre o id é somente para você, não mencione nada sobre isso ao "
            f"usuário. As preferências dele são: "
            f"{', '.join(preferences) or 'nenhuma preferência registrada'}. "
            f"Histórico de compras: {history}. "
            f"Pergunta: {question}"
            f"Responda na mesma língua em que foi feita a pergunta."
            f"Sempre fale com o usuário se dirigindo diretamente a ele, "
            f"não se refira a ele em terceira pessoa, como se estivesse "
            f"falando de outra pessoa."
            f" Dê respostas com no máximo 500 caracteres."
        )

        gemini_response = user_decision.send_message(prompt)
        response = gemini_response.text

        save_log(user_id, history, response)

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


if __name__ == '__main__':
    app.run(debug=True)
