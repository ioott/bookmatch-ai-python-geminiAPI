def recommend_fiction(user_id: int) -> str:
    """
    Recomenda livros de ficção ao usuário.
    """
    return (
        f"Usuário {user_id}, já que você gosta de ficção, recomendamos estes "
        f"lançamentos que você vai adorar!\n"
        "- A Menina que Roubava Livros, de Markus Zusak\n"
        "- Onde Cantam os Pássaros, de Evie Wyld\n"
        "- A Paciente Silenciosa, de Alex Michaelides"
    )


def recommend_non_fiction(user_id: int) -> str:
    """
    Recomenda livros de não ficção ao usuário.
    """
    return (
        f"Usuário {user_id}, já que você gosta de não-ficção, recomendamos "
        f"estes lançamentos que você vai adorar!\n"
        "- Sapiens: Uma Breve História da Humanidade, de Yuval Harari\n"
        "- O Poder do Hábito, de Charles Duhigg\n"
        "- Como as Democracias Morrem, de Steven Levitsky e Daniel Ziblatt"
    )


def recommend_science(user_id: int) -> str:
    """
    Recomenda livros de ciência ao usuário.
    """
    return (
        f"Usuário {user_id}, já que você gosta de ciência, recomendamos estes "
        f"lançamentos que você vai adorar!\n"
        "- Uma Breve História do Tempo, de Stephen Hawking\n"
        "- O Gene: Uma História Íntima, de Siddhartha Mukherjee\n"
        "- O Mundo Assombrado pelos Demônios, de Carl Sagan"
    )


def recommend_fantasy(user_id: int) -> str:
    """
    Recomenda livros de fantasia ao usuário.
    """
    return (
        f"Usuário {user_id}, já que você gosta de fantasia, recomendamos estes "
        f"lançamentos que você vai adorar!\n"
        "- O Nome do Vento, de Patrick Rothfuss\n"
        "- O Senhor dos Anéis, de J.R.R. Tolkien\n"
        "- A Canção do Sangue, de Anthony Ryan"
    )
