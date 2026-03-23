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


def get_registration_worksheet():
    settings = get_settings()
    client = get_gspread_client()
    spreadsheet = client.open_by_key(settings.google_sheets_spreadsheet_id)
    return spreadsheet.sheet1


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
        str(registration.course_duration_months),
        str(registration.months_paid),
        str(registration.telegram_user_id),
        registration.telegram_username or "",
        registration.status,
    ]


def append_registration_to_google_sheets(registration: Registration) -> None:
    worksheet = get_registration_worksheet()
    row = build_registration_row(registration)
    worksheet.append_row(row)


def find_row_by_reference_code(reference_code: str) -> int | None:
    worksheet = get_registration_worksheet()
    values = worksheet.col_values(1)

    for index, value in enumerate(values, start=1):
        if value == reference_code:
            return index

    return None


def update_registration_status_in_google_sheets(
    reference_code: str,
    new_status: str,
) -> bool:
    worksheet = get_registration_worksheet()
    row_number = find_row_by_reference_code(reference_code)

    if row_number is None:
        return False

    status_column = 13  # Column M
    worksheet.update_cell(row_number, status_column, new_status)
    return True


def update_course_duration_in_google_sheets(
    reference_code: str,
    duration_months: int,
) -> bool:
    worksheet = get_registration_worksheet()
    row_number = find_row_by_reference_code(reference_code)

    if row_number is None:
        return False

    duration_column = 9  # Column I
    worksheet.update_cell(row_number, duration_column, duration_months)
    return True


def update_months_paid_in_google_sheets(
    reference_code: str,
    months_paid: int,
) -> bool:
    worksheet = get_registration_worksheet()
    row_number = find_row_by_reference_code(reference_code)

    if row_number is None:
        return False

    months_paid_column = 10  # Column J
    worksheet.update_cell(row_number, months_paid_column, months_paid)
    return True