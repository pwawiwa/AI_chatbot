#!/usr/bin/env python3
"""
Test mengirim pesan langsung ke nomor HP user
"""
import os
from dotenv import load_dotenv
from whatsapp_api import send_text_message

load_dotenv()

def test_direct_message():
    """Test mengirim pesan langsung"""
    print("📱 Testing Direct Message to Your Phone...")
    
    # GANTI DENGAN NOMOR HP KAMU (format: 628xxxxxxxxxx)
    your_phone_number = "6281234567890"  # Ganti dengan nomor HP kamu
    
    print(f"📞 Sending message to: {your_phone_number}")
    print("⚠️  Make sure this number is added to allowed list in Meta Developer Console")
    
    success, response = send_text_message(
        to_number=your_phone_number,
        text="Halo! Ini test dari WhatsApp Bot Almeera ✨\n\nBot sudah siap menerima pesan dan memberikan rekomendasi treatment yang sesuai! 💖"
    )
    
    if success:
        print("✅ Message sent successfully!")
        print(f"Response: {response}")
        print("\n🎉 Bot is ready! Now you can send messages to your WhatsApp Business number")
    else:
        print("❌ Failed to send message")
        print(f"Error: {response}")
        print("\n💡 Make sure:")
        print("1. Your phone number is added to allowed list in Meta Developer Console")
        print("2. WhatsApp Business API is properly configured")
        print("3. Access token is valid")

if __name__ == "__main__":
    test_direct_message()
