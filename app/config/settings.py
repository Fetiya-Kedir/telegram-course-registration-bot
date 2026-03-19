from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class Settings:
    bot_token: str
    admin_ids: list[int]
    admin_username: str
    google_sheets_spreadsheet_id: str
    google_service_account_file: str


def get_settings() -> Settings:
    bot_token = os.getenv("BOT_TOKEN", "")
    raw_admin_ids = os.getenv("ADMIN_IDS", "")
    admin_username = os.getenv("ADMIN_USERNAME", "").strip()
    google_sheets_spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID", "").strip()
    google_service_account_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "").strip()

    admin_ids = [int(x.strip()) for x in raw_admin_ids.split(",") if x.strip()]

    if not bot_token:
        raise ValueError("BOT_TOKEN is missing in .env")

    if not admin_username:
        raise ValueError("ADMIN_USERNAME is missing in .env")

    if not google_sheets_spreadsheet_id:
        raise ValueError("GOOGLE_SHEETS_SPREADSHEET_ID is missing in .env")

    if not google_service_account_file:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_FILE is missing in .env")

    return Settings(
        bot_token=bot_token,
        admin_ids=admin_ids,
        admin_username=admin_username,
        google_sheets_spreadsheet_id=google_sheets_spreadsheet_id,
        google_service_account_file=google_service_account_file,
    )