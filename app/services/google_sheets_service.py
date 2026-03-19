from google.oauth2.service_account import Credentials
import gspread

from app.config.settings import get_settings
from app.database.models import Registration


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_gspread_client() -> gspread.Client:
    settings = get_settings()

    credentials = Credentials.from_service_account_file(
        settings.google_service_account_file,
        scopes=SCOPES,
    )

    return gspread.authorize(credentials)


def build_registration_row(registration: Registration) -> list[str]:
    created_at = registration.created_at.strftime("%Y-%m-%d %H:%M:%S")

    return [
        registration.reference_code or "",
        created_at,
        registration.full_name,
        registration.department,
        registration.phone,
        registration.language,
        registration.class_id,
        registration.class_name,
        str(registration.telegram_user_id),
        registration.telegram_username or "",
        registration.status,
    ]


def append_registration_to_google_sheets(registration: Registration) -> None:
    settings = get_settings()

    client = get_gspread_client()
    spreadsheet = client.open_by_key(settings.google_sheets_spreadsheet_id)
    worksheet = spreadsheet.sheet1

    row = build_registration_row(registration)
    worksheet.append_row(row)