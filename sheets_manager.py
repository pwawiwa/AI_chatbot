# sheets_manager.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_SHEETS_CREDENTIALS_PATH
from config import SPREADSHEET_ID


def get_google_sheet_client():
    """Authenticates with Google Sheets and returns a client."""
    try:
        # Use Sheets scopes only to avoid requiring Drive API
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/spreadsheets.readonly",
        ]
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
        from datetime import datetime, timedelta

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


def find_spreadsheet_containing_worksheet(client, worksheet_title):
    """Search all accessible spreadsheets and return the first spreadsheet that contains a worksheet with the given title."""
    try:
        spreadsheets = client.openall()
        for ss in spreadsheets:
            try:
                _ = ss.worksheet(worksheet_title)
                print(f"Found worksheet '{worksheet_title}' in spreadsheet '{ss.title}'.")
                return ss
            except Exception:
                continue
        print(f"Worksheet '{worksheet_title}' not found in any accessible spreadsheet.")
        return None
    except Exception as e:
        print(f"Error searching spreadsheets: {e}")
        return None


def update_birthday_reminders_for_today(spreadsheet, worksheet_name):
    """Set 'ULTAH REMINDER' to 'ULTAH HARI INI' if today's month/day matches 'Tanggal lahir'.
    Returns the number of rows updated.
    """
    try:
        from datetime import datetime
        ws = spreadsheet.worksheet(worksheet_name)
        values = ws.get_all_values()
        if not values:
            print("Worksheet is empty.")
            return 0
        headers = values[0]
        header_to_index = {h: i for i, h in enumerate(headers)}

        # Column name assumptions based on user input
        dob_col = header_to_index.get('Tanggal lahir')
        reminder_col = header_to_index.get('ULTAH REMINDER')
        bulan_col = header_to_index.get('BULAN')
        tanggal_col = header_to_index.get('TANGGAL')

        if dob_col is None and (bulan_col is None or tanggal_col is None):
            print("Required columns not found: need 'Tanggal lahir' or both 'BULAN' and 'TANGGAL'.")
            return 0
        if reminder_col is None:
            print("Required column 'ULTAH REMINDER' not found.")
            return 0

        today = datetime.now()
        today_m = today.month
        today_d = today.day

        updated = 0
        # Iterate data rows (starting at row index 1; Google Sheets rows start at 1)
        for row_idx in range(1, len(values)):
            row = values[row_idx]

            # Extract month/day from dob string if available
            mm = None
            dd = None

            if dob_col is not None and dob_col < len(row):
                raw_dob = row[dob_col].strip()
                if raw_dob:
                    # Try multiple formats
                    parsed = None
                    for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%d %m %Y'):
                        try:
                            parsed = datetime.strptime(raw_dob, fmt)
                            break
                        except Exception:
                            continue
                    if parsed:
                        mm, dd = parsed.month, parsed.day

            # Fallback to separate columns BULAN and TANGGAL
            if (mm is None or dd is None) and bulan_col is not None and tanggal_col is not None:
                try:
                    bulan_val = row[bulan_col].strip() if bulan_col < len(row) else ''
                    tanggal_val = row[tanggal_col].strip() if tanggal_col < len(row) else ''
                    if bulan_val and tanggal_val:
                        mm = int(bulan_val)
                        dd = int(tanggal_val)
                except Exception:
                    pass

            # Determine target value
            target_value = "ULTAH HARI INI" if (mm == today_m and dd == today_d) else ""

            # Current reminder value
            current_val = row[reminder_col] if reminder_col < len(row) else ''

            if current_val != target_value:
                # Google Sheets uses 1-based indexing for rows/cols
                ws.update_cell(row_idx + 1, reminder_col + 1, target_value)
                updated += 1
        print(f"Updated {updated} rows for birthday reminders.")
        return updated
    except Exception as e:
        print(f"Error updating birthday reminders: {e}")
        return 0


def open_spreadsheet_by_id(client, spreadsheet_id):
    """Open spreadsheet by known spreadsheet ID."""
    try:
        ss = client.open_by_key(spreadsheet_id)
        print(f"Opened spreadsheet by ID: {ss.title}")
        return ss
    except Exception as e:
        print(f"Error opening spreadsheet by ID: {e}")
        return None


def get_rows_where_column_equals(spreadsheet, worksheet_name, column_name, expected_value):
    """Return rows (as dicts) where a given column equals expected_value."""
    try:
        ws = spreadsheet.worksheet(worksheet_name)
        data = ws.get_all_records()
        return [row for row in data if str(row.get(column_name, '')).strip() == str(expected_value)]
    except Exception as e:
        print(f"Error filtering rows in '{worksheet_name}': {e}")
        return []