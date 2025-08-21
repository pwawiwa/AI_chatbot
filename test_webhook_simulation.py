#!/usr/bin/env python3
"""
Test script untuk mensimulasikan pesan WhatsApp ke webhook
"""
import requests
import json

def test_webhook_with_simulated_message():
    """Test webhook dengan pesan simulasi"""
    print("🧪 Testing Webhook with Simulated WhatsApp Message...")
    
    # GANTI DENGAN NOMOR HP KAMU (format: 628xxxxxxxxxx)
    user_phone_number = "6281234567890"  # Ganti dengan nomor HP kamu
    
    # Simulasi payload WhatsApp dengan pesan berbeda
    simulated_payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "123456789",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "1234567890",
                                "phone_number_id": "987654321"
                            },
                            "messages": [
                                {
                                    "from": user_phone_number,  # Nomor pengirim (HP kamu)
                                    "id": "test_message_id_2",
                                    "timestamp": "1234567890",
                                    "type": "text",
                                    "text": {
                                        "body": "Halo kak, mau tanya soal treatment filler"
                                    }
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }
    
    # Kirim ke webhook
    try:
        response = requests.post(
            "http://127.0.0.1:8080/webhook",
            json=simulated_payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook processed successfully!")
            print("📱 Bot should have sent a response (check server logs)")
            print(f"📞 Simulated message from: {user_phone_number}")
        else:
            print("❌ Webhook failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_webhook_with_simulated_message()
