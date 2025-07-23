import os
from datetime import datetime

# Garante a compatibilidade do caminho do log entre os ambientes
LOG_FILE_PATH = "/tmp/recommender.log"
if os.name == 'nt':
    LOG_FILE_PATH = "recommender.log"


def save_log(user_id: int, history: dict, response: str):
    log_entry = (
        f"[{datetime.now().isoformat(sep=' ', timespec='seconds')}]\n"
        f"Usuário: {user_id}\n"
        f"Histórico: {history}\n"
        f"Recomendação: {response.strip()}\n"
        f"{'-'*40}\n"
    )
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(log_entry)


def get_user_history(user_id: int) -> dict:
    history = {}
    try:
        with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
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


def get_all_users() -> dict:
    users = {}
    try:
        with open(LOG_FILE_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

        current_user = None

        for i, line in enumerate(lines):

            if line.startswith("Usuário:"):
                current_user = int(line.split(":")[1].strip())
            elif line.startswith("Histórico:") and current_user is not None:
                history = eval(line.split(":", 1)[1].strip())
                users[current_user] = history

    except FileNotFoundError:
        pass

    return users
