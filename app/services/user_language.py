user_languages: dict[int, str] = {}


def set_user_language(user_id: int, lang: str) -> None:
    user_languages[user_id] = lang


def get_user_language(user_id: int) -> str:
    return user_languages.get(user_id, "en")