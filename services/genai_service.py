import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def configure_genai():
    """
    Configura a chave de API e inicializa o modelo Gemini.
    """
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise EnvironmentError(
            "❌ A variável de ambiente GOOGLE_API_KEY não está definida."
        )

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        print("✅ Chave da API configurada com sucesso.")
        return model

    except Exception as e:
        print(f"❌ Falha ao configurar a chave da API: {e}")
        return None
