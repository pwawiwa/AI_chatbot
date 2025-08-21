import os
import hmac
import hashlib
import datetime
from flask import Flask, request, jsonify, Response
from dotenv import load_dotenv
from llm_manager import get_llm_response, moderate_content
from data_loader import load_prices_data
from whatsapp_api import send_text_message


app = Flask(__name__)
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "verify_token_dev")
APP_SECRET = os.getenv("WHATSAPP_APP_SECRET", "")
# Load prices data with fallback
try:
    PRICES = load_prices_data("Price List/prices_august.json")
    if not PRICES:
        print("⚠️  No prices data loaded, using empty list")
        PRICES = []
except Exception as e:
    print(f"❌ Error loading prices data: {e}")
    PRICES = []


def verify_signature(request_body: bytes, signature: str) -> bool:
    if not APP_SECRET or not signature:
        return True
    try:
        mac = hmac.new(APP_SECRET.encode("utf-8"), msg=request_body, digestmod=hashlib.sha256)
        expected = "sha256=" + mac.hexdigest()
        return hmac.compare_digest(expected, signature)
    except Exception:
        return False


@app.route("/", methods=["GET"])
def health():
    try:
        return jsonify({
            "status": "ok",
            "message": "WhatsApp Bot Almeera is running",
            "timestamp": str(datetime.datetime.now())
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/webhook", methods=["GET"])
def webhook_verify():
    # Support Meta hub.* params
    mode = request.args.get("hub.mode", request.args.get("mode", ""))
    raw_token = request.args.get("hub.verify_token", request.args.get("token", ""))
    challenge = request.args.get("hub.challenge", request.args.get("challenge", ""))

    # Normalize (strip whitespace) to avoid trailing-space mismatches
    token = (raw_token or "").strip()
    expected = (VERIFY_TOKEN or "").strip()

    # Debug (non-sensitive): print lengths only
    print(f"[WEBHOOK VERIFY] mode={mode} recv_token_len={len(token)} env_token_len={len(expected)}")

    if mode == "subscribe" and token == expected:
        return Response(challenge, status=200, mimetype="text/plain")
    return Response("Forbidden", status=403)


@app.route("/webhook", methods=["POST"])
def webhook_receive():
    sig = request.headers.get("X-Hub-Signature-256", "")
    raw = request.data or b""
    if not verify_signature(raw, sig):
        return Response("Invalid signature", status=401)

    payload = request.get_json(silent=True) or {}
    print(f"[WEBHOOK POST] Received payload: {payload}")
    
    try:
        for entry in payload.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                for msg in value.get("messages", []):
                    from_number = msg.get("from")
                    msg_type = msg.get("type")
                    print(f"[MESSAGE] From: {from_number}, Type: {msg_type}")
                    
                    if msg_type == "text":
                        text = msg.get("text", {}).get("body", "")
                        print(f"[TEXT] Content: {text}")
                        
                        flagged, _ = moderate_content(text)
                        if flagged:
                            print(f"[MODERATION] Message flagged as inappropriate")
                            success, response = send_text_message(from_number, "Maaf, pesannya kurang sesuai ya. Coba pakai kata yang lebih sopan ✨")
                            print(f"[SEND] Moderation response - Success: {success}, Response: {response}")
                            continue
                        
                        messages = [{"role": "user", "content": f"Pasien bertanya: {text}"}]
                        reply = get_llm_response(messages, PRICES)
                        print(f"[LLM] Reply: {reply}")
                        
                        success, response = send_text_message(from_number, reply)
                        print(f"[SEND] LLM response - Success: {success}, Response: {response}")
                    else:
                        print(f"[OTHER] Non-text message type: {msg_type}")
                        success, response = send_text_message(from_number, "Minra terima pesannya yaa. Untuk saat ini, kirim teks dulu ya ✨")
                        print(f"[SEND] Other message response - Success: {success}, Response: {response}")
    except Exception as e:
        print(f"[ERROR] Exception in webhook processing: {e}")
        import traceback
        traceback.print_exc()
    
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    # Production settings
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    print(f"🚀 Starting server on port {port}")
    print(f"📡 Server will be available at: http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
