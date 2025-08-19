# main.py

from config import OPENAI_API_KEY
from data_loader import load_prices_data
import openai
# from sheets_manager import get_google_sheet_client, open_spreadsheet, get_worksheet_data, append_row_to_worksheet, find_patient_by_rm_number, get_upcoming_treatments, get_upcoming_birthdays
from llm_manager import get_llm_response, moderate_content

PRICES_FILE = "Harga Agustus/prices_august.json"
# GOOGLE_SHEET_NAME = "WhatsApp Chatbot Data"
# PATIENT_WORKSHEET_NAME = "Patients"
# CONSULTATION_WORKSHEET_NAME = "Consultations"
# ORDER_WORKSHEET_NAME = "Orders"

def main():
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY not found in .env file.")
        return

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    print("OpenAI client initialized.")

    prices_data = load_prices_data(PRICES_FILE)
    if prices_data:
        print(f"Successfully loaded {len(prices_data)} treatment prices.")
    else:
        print("Failed to load prices data.")
        return # Exit if prices data is critical and not loaded

    # # Google Sheets Integration for Patient Identification
    # gs_client = get_google_sheet_client()
    # if gs_client:
    #     spreadsheet = open_spreadsheet(gs_client, GOOGLE_SHEET_NAME)
    #     if spreadsheet:
    #         print("\n--- Patient Identification ---")
    #         patient_type = input("Are you a new patient or an existing patient? (new/existing): ").lower()

    #         if patient_type == "new":
    #             print("Please provide your details to register.")
    #             name = input("Enter your name: ")
    #             import uuid
    #             rm_number = str(uuid.uuid4())[:8]
    #             new_patient_data = [rm_number, name, "", "", ""]
    #             if append_row_to_worksheet(spreadsheet, PATIENT_WORKSHEET_NAME, new_patient_data):
    #                 print(f"New patient {name} registered with RM Number: {rm_number}")
    #                 current_patient = {"RM Number": rm_number, "Name": name}
    #             else:
    #                 print("Failed to register new patient.")
    #                 current_patient = None

    #         elif patient_type == "existing":
    #             rm_number = input("Please enter your RM Number: ")
    #             patient_record = find_patient_by_rm_number(spreadsheet, PATIENT_WORKSHEET_NAME, rm_number)
    #             if patient_record:
    #                 print(f"Welcome back, {patient_record[1]}! Your details: {patient_record}")
    #                 current_patient = {"RM Number": patient_record[0], "Name": patient_record[1]}
    #             else:
    #                 print("RM Number not found. Please try again or register as a new patient.")
    #                 current_patient = None
    #         else:
    #             print("Invalid input. Please type 'new' or 'existing'.")
    #             current_patient = None

    #         if current_patient:
    #             print("\n--- Initial Consultation --- ")
    #             patient_complaint = input("Hello! How can I help you today? Please describe your skin concerns or what kind of treatment you are looking for: ")

    #             flagged, categories = moderate_content(patient_complaint)
    #             if flagged:
    #                 print(f"Warning: Your input contains inappropriate content: {categories}. Please rephrase your query.")
    #                 return # Exit the main function or handle as needed

    #             prompt = f"Pasien bertanya: {patient_complaint}."

    #             llm_response = get_llm_response(prompt, prices_data)
    #             print("Bot Response:", llm_response)

    #             # Simulate Relay Chat Patient <-> Doctor
    #             print("\n--- Doctor Consultation --- ")
    #             needs_doctor = input("Do you need to consult with a doctor regarding your concerns? (yes/no): ").lower()

    #             if needs_doctor == "yes":
    #                 consultation_data = [current_patient["RM Number"], current_patient["Name"], patient_complaint, llm_response, "Pending"]
    #                 if append_row_to_worksheet(spreadsheet, CONSULTATION_WORKSHEET_NAME, consultation_data):
    #                     print("Your request has been forwarded to a doctor. We will get back to you shortly.")
    #                 else:
    #                     print("Failed to forward your request to a doctor.")
    #             else:
    #                 print("Okay, if you have any other questions, feel free to ask!")

    #             # Simulate Order & Jadwal
    #             print("\n--- Order and Scheduling ---")
    #             place_order = input("Would you like to place an order or schedule a treatment? (yes/no): ").lower()

    #             if place_order == "yes":
    #                 treatment_name = input("Which treatment would you like to order/schedule?: ")
    #                 scheduled_date = input("On what date would you like to schedule it (YYYY-MM-DD)?: ")

    #                 # Moderating order input
    #                 order_input_text = f"Treatment: {treatment_name}, Date: {scheduled_date}"
    #                 flagged_order, categories_order = moderate_content(order_input_text)
    #                 if flagged_order:
    #                     print(f"Warning: Your order details contain inappropriate content: {categories_order}. Please re-enter your order.")
    #                     return # Exit or handle as needed

    #                 order_data = [current_patient["RM Number"], current_patient["Name"], treatment_name, scheduled_date, "Ordered"]
    #                 if append_row_to_worksheet(spreadsheet, ORDER_WORKSHEET_NAME, order_data):
    #                     print(f"Order for {treatment_name} on {scheduled_date} placed successfully for {current_patient["Name"]}.")
    #                 else:
    #                     print("Failed to place order.")
    #             else:
    #                 print("No order placed at this time.")

    #     else:
    #         print("Failed to open Google Spreadsheet.")
    # else:
    #     print("Failed to authenticate with Google Sheets.")

    # Simulate Automatic Reminders (Daily Check - can be a separate cron job in real app)
    # print("\n--- Daily Reminders Check ---")
    # if gs_client and spreadsheet:
    #     upcoming_treatments = get_upcoming_treatments(spreadsheet, ORDER_WORKSHEET_NAME, days_in_advance=1)
    #     if upcoming_treatments:
    #         print("Upcoming Treatment Reminders:")
    #         for treatment in upcoming_treatments:
    #             print(f"  Reminder: {treatment['Name']} has a treatment scheduled for {treatment['Scheduled Date']}. Treatment: {treatment['Treatment Name']}")
    #     else:
    #         print("No upcoming treatments for tomorrow.")

    #     upcoming_birthdays = get_upcoming_birthdays(spreadsheet, PATIENT_WORKSHEET_NAME, days_in_advance=7)
    #     if upcoming_birthdays:
    #         print("Upcoming Birthday Reminders:")
    #         for patient in upcoming_birthdays:
    #             print(f"  Birthday Reminder: Happy Birthday, {patient['Name']}! Don't forget to send a Birthday Treat.")
    #     else:
    #         print("No upcoming birthdays in the next 7 days.")

    # Temporary direct LLM interaction for testing
    print("\n--- LLM Chat Test ---")
    messages = [] # Initialize conversation history

    while True:
        user_input = input("You (type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        flagged, categories = moderate_content(user_input)
        if flagged:
            print(f"Bot: Warning! Input contains inappropriate content: {categories}. Please rephrase.")
            continue

        messages.append({"role": "user", "content": user_input}) # Add user message to history

        llm_response = get_llm_response(messages, prices_data)
        print("Bot:", llm_response)
        messages.append({"role": "assistant", "content": llm_response}) # Add bot response to history

if __name__ == "__main__":
    main()