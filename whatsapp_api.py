import os
import requests
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_TOKEN_ACCESS = os.getenv("WHATSAPP_TOKEN_ACCESS")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")  # WhatsApp Phone Number ID
GRAPH_API_BASE = "https://graph.facebook.com/v22.0"


def send_text_message(to_number: str, text: str) -> tuple[bool, str]:
    try:
        url = f"{GRAPH_API_BASE}/{PHONE_NUMBER}/messages"
        headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN_ACCESS}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {"body": text},
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code // 100 == 2:
            return True, resp.text
        return False, resp.text
    except Exception as e:
        return False, str(e)


def send_template_message(to_number: str, template_name: str, language_code: str = "en_US", components=None) -> tuple[bool, str]:
    try:
        url = f"{GRAPH_API_BASE}/{PHONE_NUMBER}/messages"
        headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN_ACCESS}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code},
            },
        }
        if components:
            payload["template"]["components"] = components
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code // 100 == 2:
            return True, resp.text
        return False, resp.text
    except Exception as e:
        return False, str(e)
