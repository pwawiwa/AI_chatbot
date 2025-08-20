from sheets_manager import get_google_sheet_client, open_spreadsheet_by_id, get_rows_where_column_equals
from config import SPREADSHEET_ID

WORKSHEET_NAME = "leads_pbg"


def main():
    client = get_google_sheet_client()
    if not client:
        print("Failed to authenticate with Google Sheets client.")
        return

    if not SPREADSHEET_ID:
        print("SPREADSHEET_ID is not set in environment.")
        return

    spreadsheet = open_spreadsheet_by_id(client, SPREADSHEET_ID)
    if not spreadsheet:
        print("Unable to open spreadsheet by ID.")
        return

    rows = get_rows_where_column_equals(spreadsheet, WORKSHEET_NAME, "ULTAH REMINDER", "ULTAH HARI INI")
    if not rows:
        print("No birthdays today.")
        return

    print("Nama, No. Whatsapp")
    for row in rows:
        name = str(row.get("Nama", "")).strip()
        phone = str(row.get("No. Whatsapp", "")).strip()
        print(f"{name}, {phone}")


if __name__ == "__main__":
    main()