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
