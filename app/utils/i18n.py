import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
I18N_DIR = BASE_DIR / "i18n"

SUPPORTED_LANGUAGES = {"en", "am"}
DEFAULT_LANGUAGE = "en"

_translations: dict[str, dict[str, str]] = {}


def load_translations() -> None:
    global _translations

    for lang in SUPPORTED_LANGUAGES:
        file_path = I18N_DIR / f"{lang}.json"
        with open(file_path, "r", encoding="utf-8") as f:
            _translations[lang] = json.load(f)


def t(lang: str, key: str) -> str:
    lang = lang if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
    return _translations.get(lang, {}).get(key, key)