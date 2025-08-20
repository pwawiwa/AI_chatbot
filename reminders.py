from sheets_manager import get_google_sheet_client, find_spreadsheet_containing_worksheet, update_birthday_reminders_for_today, open_spreadsheet_by_id
from config import SPREADSHEET_ID

WORKSHEET_NAME = "leads_pbg"


def main():
    client = get_google_sheet_client()
    if not client:
        print("Failed to authenticate with Google Sheets client.")
        return

    spreadsheet = None
    if SPREADSHEET_ID:
        spreadsheet = open_spreadsheet_by_id(client, SPREADSHEET_ID)
    if not spreadsheet:
        spreadsheet = find_spreadsheet_containing_worksheet(client, WORKSHEET_NAME)
    if not spreadsheet:
        print(f"Worksheet '{WORKSHEET_NAME}' not found in accessible spreadsheets.")
        print("Tip: Set SPREADSHEET_ID in .env to avoid Drive API listing.")
        return

    updated = update_birthday_reminders_for_today(spreadsheet, WORKSHEET_NAME)
    print(f"Done. Rows updated: {updated}")


if __name__ == "__main__":
    main()