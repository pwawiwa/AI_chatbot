# README.md: Beauty Clinic WhatsApp Chatbot

This project is a WhatsApp-based chatbot for a beauty clinic (klinik kecantikan). It handles customer inquiries, provides information on services and pricelist (daftar harga), and responds intelligently using an LLM (Large Language Model). Currently, only the core chatbot functionality is implemented. Features like birthday reminders, general reminders, and forwarding chats to doctors are planned but not yet integrated.

The chatbot uses Flask as the web server, WhatsApp Cloud API for messaging, and Ngrok for exposing the local server to the internet. Data like API keys are stored in `.env`. Additional components include Google Sheets integration for managing pricelist and other data.

## Project Structure

- **.venv/**: Virtual environment for Python dependencies.
- **credentials/**: Folder for sensitive credentials (e.g., service account keys for Google Sheets).
- **cogent-sweep-465/**: Possibly a generated or temporary folder (ignore or review if needed).
- **docs/**: Documentation folder.
- **Harga Agustus/**: Folder containing August pricelist data.
- **prices_august...**: Specific pricelist files (e.g., Excel or CSV for services and prices).
- **.env**: Environment variables file (API keys, tokens, etc.). Do not commit to Git.
- **.gitignore**: Git ignore file to exclude sensitive or temporary files.
- **birthday_messenger.py**: Script for sending birthday messages (not yet integrated).
- **config.py**: Configuration settings (e.g., API endpoints, constants).
- **data_loader.py**: Loads data from sources like Google Sheets or local files (e.g., pricelist).
- **list_birthdays.txt**: Text file listing birthdays (for future reminders).
- **llm_manager.py**: Manages LLM interactions (e.g., generating responses for chatbot).
- **main.py**: Main entry point to run the application.
- **reminders.py**: Script for handling reminders (not yet implemented).
- **requirements.txt**: List of Python dependencies.
- **server_flask.py**: Flask server for handling WhatsApp webhooks.
- **sheets_manager.py**: Manages Google Sheets integration (e.g., for pricelist updates).
- **whatsapp_api.py**: Functions for sending/receiving WhatsApp messages.

## Prerequisites

- Python 3.8+ installed.
- Ngrok account (for exposing the server).
- Meta Developers account with WhatsApp Business API app (for tokens and Phone Number ID).
- Google Cloud account (if using Sheets; need service account credentials in `credentials/`).
- All API keys, tokens, and secrets in `.env` (e.g., WHATSAPP_TOKEN_ACCESS, PHONE_NUMBER, GOOGLE_SHEETS_ID, etc.).

## Setup Instructions

1. **Clone the Repository** (if applicable):
   ```
   git clone <repo-url>
   cd <project-folder>
   ```

2. **Set Up Virtual Environment**:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```
   Common libraries: flask, requests, python-dotenv, google-api-python-client (for Sheets), openai or similar (for LLM).

4. **Configure .env**:
   Create or edit `.env` with your values:
   ```
   WHATSAPP_TOKEN_ACCESS=your_whatsapp_token
   PHONE_NUMBER=your_whatsapp_phone_id
   VERIFY_TOKEN=your_webhook_verify_token
   GOOGLE_SHEETS_CREDENTIALS_PATH=credentials/service_account.json
   GOOGLE_SHEETS_ID=your_sheet_id_for_pricelist
   LLM_API_KEY=your_llm_api_key (e.g., OpenAI)
   ```
   Ensure all sensitive data is here.

5. **Load Pricelist Data**:
   - Place pricelist files in `Harga Agustus/` or configure `sheets_manager.py` to pull from Google Sheets.
   - Run `data_loader.py` if needed to preload data: `python data_loader.py`.

6. **Set Up WhatsApp Webhook**:
   - In Meta Developers portal: Configure webhook URL (from Ngrok) in WhatsApp > Configuration > Webhooks.
   - Subscribe to "messages" event.
   - Add test phone numbers to avoid "Recipient not in allowed list" error.

## Running the Application

1. **Start the Flask Server**:
   ```
   python server_flask.py
   ```
   Or if main.py orchestrates everything:
   ```
   python main.py
   ```
   Server runs on `http://localhost:5000` (or configured port).

2. **Expose with Ngrok**:
   ```
   ngrok http 5000
   ```
   Copy the public URL (e.g., `https://abc.ngrok.io`) and update in Meta portal as webhook callback: `<ngrok-url>/webhook`.

3. **Test the Chatbot**:
   - Send a message to your WhatsApp Business number from a test phone.
   - The server receives it via webhook, processes with LLM (e.g., for beauty queries or pricelist), and replies.
   - Check console logs for incoming/outgoing messages.

## Current Features

- **Chatbot**: Receives messages, generates responses using LLM (e.g., about services, appointments, pricelist).
- **Pricelist Integration**: Loads prices from files or Sheets; chatbot can query and share them.

## Planned Features (Not Implemented)

- **Reminders**: Use `reminders.py` to send automated reminders (e.g., appointments) via WhatsApp.
- **Birthday Messenger**: Integrate `birthday_messenger.py` to send greetings based on `list_birthdays.txt`.
- **Forward Chat to Doctor**: Add logic in `server_flask.py` or `whatsapp_api.py` to forward complex queries to a doctor's WhatsApp.
- **Full Integration**: Tie everything in `main.py` (e.g., scheduled tasks for reminders).

To implement these:
- For reminders: Use libraries like schedule or APScheduler; call WhatsApp API functions.
- For forwarding: Add conditional logic in webhook handler to send messages to doctor's number.
- Update `llm_manager.py` to handle specific intents (e.g., "forward to doctor").

## Troubleshooting

- **Error 131030 (Recipient not in allowed list)**: Add test numbers in Meta portal.
- **No Response in WhatsApp**: Check Ngrok URL, webhook verification, and server logs.
- **Data Loading Issues**: Verify Google Sheets credentials and IDs.
- **LLM Errors**: Ensure API key is valid; test `llm_manager.py` separately.
- **Security**: Use HTTPS via Ngrok; never expose `.env`.

## Additional Resources

- WhatsApp Cloud API: [Docs](https://developers.facebook.com/docs/whatsapp/cloud-api)
- Flask: [Docs](https://flask.palletsprojects.com/)
- Google Sheets API: [Docs](https://developers.google.com/sheets/api)
- Ngrok: [Docs](https://ngrok.com/docs)

If you need help implementing the planned features or debugging, provide more details!