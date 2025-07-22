from datetime import datetime


def save_log(user_id: int, history: dict, response: str):
    log_entry = (
        f"[{datetime.now().isoformat(sep=' ', timespec='seconds')}]\n"
        f"Usuário: {user_id}\n"
        f"Histórico: {history}\n"
        f"Recomendação: {response.strip()}\n"
        f"{'-'*40}\n"
    )
    with open("recommender.log", "a", encoding="utf-8") as f:
        f.write(log_entry)


def get_user_history(user_id: int) -> dict:
    """
    Lê o arquivo recommender.log e retorna o último histórico do usuário.
    """
    history = {}

    try:
        with open("recommender.log", "r", encoding="utf-8") as f:
            lines = f.readlines()

        current_user = None
        
        for line in lines:
            if line.startswith("Usuário:"):
                current_user = int(line.split(":")[1].strip())
            elif line.startswith("Histórico:") and current_user == user_id:
                history = eval(line.split(":", 1)[1].strip())

    except FileNotFoundError:
        pass

    return history
