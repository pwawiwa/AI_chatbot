## Milestone 1 — Core AI Chatbot (Local)

What we built
- Project structure: `main.py`, `config.py`, `data_loader.py`, `llm_manager.py`, `sheets_manager.py`
- Treatment data loader: pulls from `Harga Agustus/prices_august.json`
- LLM chat (Bahasa Indonesia): girly, casual, elegant tone; minimal if-else; suggestions based on treatment data
- Conversation memory: passes full message history to LLM for contextual replies
- Content moderation: basic filtering using OpenAI moderation
- Local chat loop for testing (Sheets disabled by default)
- Google Sheets utilities (service account): open by Spreadsheet ID, read/write helpers
- Birthday automation: update “ULTAH REMINDER” when today == “Tanggal lahir”; list birthdays; generate birthday messages (printed only)

Tested locally
- LLM chat suggests relevant treatments and maintains context
- Sheets access via service account using `SPREADSHEET_ID`
- Scripts:
  - `reminders.py`: update “ULTAH REMINDER” in worksheet `leads_pbg`
  - `list_birthdays_today.py`: print Nama + No. Whatsapp for rows with “ULTAH HARI INI”
  - `birthday_messenger.py`: generate personalized birthday messages (console only)

How to run locally (summary)
- Requirements: `pip install -r requirements.txt`
- `.env`:
  - `OPENAI_API_KEY="..."`
  - `GOOGLE_SHEETS_CREDENTIALS_PATH="credentials/<service-account>.json"`
  - `SPREADSHEET_ID="<Google Sheet ID>"`
- Run LLM chat: `python main.py`
- Birthdays:
  - `python reminders.py`
  - `python list_birthdays_today.py`
  - `python birthday_messenger.py`

Sheets assumptions (worksheet: `leads_pbg`)
- Columns: `Nomor RM`, `Nama`, `Alamat`, `Pekerjaan`, `Tanggal lahir`, `No. Whatsapp`, `ULTAH REMINDER`, `UMUR`, `BULAN`, `TANGGAL`, `TAHUN`, etc.
- Rule: set `ULTAH REMINDER` to "ULTAH HARI INI" if today’s month/day matches `Tanggal lahir` (or matches `BULAN` and `TANGGAL` when present).

Next milestones
1) WhatsApp API (receive + send)
- Webhook receiver for customer messages (text/media)
- Number normalization (+62), media download URL handling
- Message router → LLM consultation → optional doctor relay

2) Forward chat to doctor
- Persist patient → doctor threads in Sheets (worksheet `Consultations`)
- Store message content + links (for media), preserve ordering
- LLM summary of patient complaint for quick review

3) Persist chat + orders in Sheets
- Log customer messages (raw + summary) per session
- When customer orders, write treatment + `tanggal` ke worksheet `Orders`
- Add daily reminder job to read Orders and compose reminders

4) Hardening & Ops
- Secrets: `.env` only; never commit creds/data
- Errors & retries for Sheets/LLM
- Unit tests for data loaders + prompt helpers
- Deployment plan (later): WhatsApp endpoint + worker for reminders

Notes
- To avoid Drive listing, we open Sheets by ID (preferred). Enable Drive API only if you need search/open by name.
- Images/media: store links in Sheets; actual bytes are not stored.