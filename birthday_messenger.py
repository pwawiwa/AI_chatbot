from sheets_manager import get_google_sheet_client, open_spreadsheet_by_id, update_birthday_reminders_for_today, get_rows_where_column_equals
from config import SPREADSHEET_ID
from llm_manager import get_llm_response
from data_loader import load_prices_data

WORKSHEET_NAME = "leads_pbg"
PRICES_FILE = "Harga Agustus/prices_august.json"


def build_birthday_prompt(name):
    return (
        f"Buatkan pesan ucapan ulang tahun singkat dan manis untuk pasien bernama {name}. "
        "Gunakan Bahasa Indonesia yang girly, casual, elegan, dan hangat. "
        "Ajak pasien untuk menikmati Birthday Treat di Almeera dengan nada lembut (tanpa memaksa). "
        "Batasi 2-3 kalimat saja."
    )


def main():
    # Load treatment data for potential cross-sell in system prompt
    prices_data = load_prices_data(PRICES_FILE) or []

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

    # Update reminders first
    update_birthday_reminders_for_today(spreadsheet, WORKSHEET_NAME)

    # Fetch rows where ULT AH REMINDER == 'ULTAH HARI INI'
    rows = get_rows_where_column_equals(spreadsheet, WORKSHEET_NAME, "ULTAH REMINDER", "ULTAH HARI INI")
    if not rows:
        print("No birthdays today.")
        return

    print(f"Found {len(rows)} birthdays today. Generating messages...\n")

    for row in rows:
        name = row.get("Nama", "Kak")
        phone = row.get("No. Whatsapp", "-")

        # Build conversation for contextual LLM message
        messages = [
            {"role": "user", "content": build_birthday_prompt(name) }
        ]
        response = get_llm_response(messages, prices_data)
        print("==== Message ====")
        print(f"To: {phone} | Name: {name}")
        print(response)
        print()


if __name__ == "__main__":
    main()