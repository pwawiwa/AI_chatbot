#!/usr/bin/env python3
"""
Simple test untuk WhatsApp API - TIDAK mengirim ke ultah reminder
"""
import os
from dotenv import load_dotenv
from whatsapp_api import send_text_message

load_dotenv()

def test_simple_message():
    """Test mengirim pesan sederhana"""
    print("🧪 Testing WhatsApp API - Simple Message...")
    
    # Test dengan text message ke nomor test (ganti dengan nomor kamu)
    test_number = "6281234567890"  # Ganti dengan nomor test kamu
    
    success, response = send_text_message(
        to_number=test_number,
        text="Halo! Ini test dari WhatsApp Bot Almeera ✨"
    )
    
    if success:
        print("✅ Text message sent successfully!")
        print(f"Response: {response}")
    else:
        print("❌ Failed to send text message")
        print(f"Error: {response}")
        
    print("\n📝 Note: Ganti nomor test di script ini dengan nomor kamu untuk testing")

if __name__ == "__main__":
    test_simple_message()
