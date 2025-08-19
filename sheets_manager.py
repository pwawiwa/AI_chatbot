# sheets_manager.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_SHEETS_CREDENTIALS_PATH

def get_google_sheet_client():
    """Authenticates with Google Sheets and returns a client."""
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDENTIALS_PATH, scope)
        client = gspread.authorize(creds)
        print("Google Sheets client authenticated successfully.")
        return client
    except Exception as e:
        print(f"Error authenticating with Google Sheets: {e}")
        return None

def open_spreadsheet(client, spreadsheet_name):
    """Opens a spreadsheet by name."""
    try:
        spreadsheet = client.open(spreadsheet_name)
        print(f"Spreadsheet '{spreadsheet_name}' opened successfully.")
        return spreadsheet
    except Exception as e:
        print(f"Error opening spreadsheet '{spreadsheet_name}': {e}")
        return None

def get_worksheet_data(spreadsheet, worksheet_name):
    """Retrieves all data from a specified worksheet."""
    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
        data = worksheet.get_all_records()
        print(f"Data from worksheet '{worksheet_name}' retrieved successfully.")
        return data
    except Exception as e:
        print(f"Error retrieving data from worksheet '{worksheet_name}': {e}")
        return None

def append_row_to_worksheet(spreadsheet, worksheet_name, row_data):
    """Appends a new row to a specified worksheet."""
    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
        worksheet.append_row(row_data)
        print(f"Row appended to worksheet '{worksheet_name}' successfully.")
        return True
    except Exception as e:
        print(f"Error appending row to worksheet '{worksheet_name}': {e}")
        return False

def find_patient_by_rm_number(spreadsheet, worksheet_name, rm_number):
    """Finds a patient record by RM number."""
    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
        # Assuming 'RM Number' is the header for the RM numbers column
        cell = worksheet.find(rm_number, in_column=1)  # Assuming RM number is in the first column
        row_values = worksheet.row_values(cell.row)
        print(f"Patient with RM number {rm_number} found.")
        return row_values
    except gspread.exceptions.CellNotFound:
        print(f"Patient with RM number {rm_number} not found.")
        return None
    except Exception as e:
        print(f"Error finding patient by RM number: {e}")
        return None

def update_worksheet_cell(spreadsheet, worksheet_name, row, col, value):
    """Updates a specific cell in a worksheet."""
    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
        worksheet.update_cell(row, col, value)
        print(f"Cell ({row}, {col}) in worksheet '{worksheet_name}' updated successfully.")
        return True
    except Exception as e:
        print(f"Error updating cell ({row}, {col}) in worksheet '{worksheet_name}': {e}")
        return False

def get_upcoming_treatments(spreadsheet, worksheet_name, days_in_advance=1):
    """Retrieves upcoming treatments from a specified worksheet.
    Assumes 'Scheduled Date' column for dates and 'Status' column for status.
    """
    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
        data = worksheet.get_all_records()
        upcoming_treatments = []
        from datetime import datetime, timedelta

        today = datetime.now().date()
        for row in data:
            try:
                # Assuming 'Scheduled Date' is the column name for treatment dates
                scheduled_date_str = row.get('Scheduled Date')
                status = row.get('Status')
                if scheduled_date_str and status and status == "Ordered":
                    scheduled_date = datetime.strptime(scheduled_date_str, '%Y-%m-%d').date()
                    if today <= scheduled_date <= today + timedelta(days=days_in_advance):
                        upcoming_treatments.append(row)
            except ValueError:
                print(f"Warning: Invalid date format in row: {row}")
                continue
        print(f"Found {len(upcoming_treatments)} upcoming treatments.")
        return upcoming_treatments
    except Exception as e:
        print(f"Error retrieving upcoming treatments: {e}")
        return None

def get_upcoming_birthdays(spreadsheet, worksheet_name, days_in_advance=7):
    """Retrieves upcoming birthdays from a specified worksheet.
    Assumes 'Birthday' column for birthdays.
    """
    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
        data = worksheet.get_all_records()
        upcoming_birthdays = []
        from datetime import datetime

        today = datetime.now()
        for row in data:
            try:
                # Assuming 'Birthday' is the column name for birthdays (e.g., YYYY-MM-DD)
                birthday_str = row.get('Birthday')
                if birthday_str:
                    # We only care about month and day for recurring birthdays
                    bday = datetime.strptime(birthday_str, '%Y-%m-%d')
                    # Check if birthday is within the next `days_in_advance` days
                    # Considering current year for comparison
                    current_year_bday = bday.replace(year=today.year)
                    if today <= current_year_bday < today + timedelta(days=days_in_advance):
                        upcoming_birthdays.append(row)
                    # Also check for next year if current date is late in the year
                    elif today > current_year_bday and today + timedelta(days=days_in_advance) > bday.replace(year=today.year + 1):
                        upcoming_birthdays.append(row)
            except ValueError:
                print(f"Warning: Invalid birthday date format in row: {row}")
                continue
        print(f"Found {len(upcoming_birthdays)} upcoming birthdays.")
        return upcoming_birthdays
    except Exception as e:
        print(f"Error retrieving upcoming birthdays: {e}")
        return None