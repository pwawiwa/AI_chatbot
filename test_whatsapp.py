#!/usr/bin/env python3
"""
Test script untuk verifikasi koneksi WhatsApp API
"""
import os
from dotenv import load_dotenv
from whatsapp_api import send_text_message, send_template_message

load_dotenv()

def test_whatsapp_connection():
    """Test koneksi WhatsApp API"""
    print("🧪 Testing WhatsApp API Connection...")
    
    # Test dengan template message (hello_world)
    print("\n1. Testing template message...")
    success, response = send_template_message(
        to_number="6281234567890",  # Ganti dengan nomor test kamu
        template_name="hello_world",
        language_code="en_US"
    )
    
    if success:
        print("✅ Template message sent successfully!")
        print(f"Response: {response}")
    else:
        print("❌ Failed to send template message")
        print(f"Error: {response}")
    
    # Test dengan text message
    print("\n2. Testing text message...")
    success, response = send_text_message(
        to_number="6281234567890",  # Ganti dengan nomor test kamu
        text="Halo! Ini test dari WhatsApp Bot Almeera ✨"
    )
    
    if success:
        print("✅ Text message sent successfully!")
        print(f"Response: {response}")
    else:
        print("❌ Failed to send text message")
        print(f"Error: {response}")

if __name__ == "__main__":
    test_whatsapp_connection()
