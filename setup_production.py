#!/usr/bin/env python3
"""
Script untuk setup environment variables production
"""
import os
from dotenv import load_dotenv

def setup_production_env():
    """Setup environment variables untuk production"""
    print("🚀 Setting up Production Environment Variables")
    print("=" * 50)
    
    # Load current .env
    load_dotenv()
    
    print("📋 Current Environment Variables:")
    print(f"WHATSAPP_TOKEN_ACCESS: {'✅ Set' if os.getenv('WHATSAPP_TOKEN_ACCESS') else '❌ Not Set'}")
    print(f"PHONE_NUMBER: {'✅ Set' if os.getenv('PHONE_NUMBER') else '❌ Not Set'}")
    print(f"WHATSAPP_VERIFY_TOKEN: {'✅ Set' if os.getenv('WHATSAPP_VERIFY_TOKEN') else '❌ Not Set'}")
    print(f"OPENAI_API_KEY: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Not Set'}")
    
    print("\n🔧 Production Setup Checklist:")
    print("1. ✅ WhatsApp Business API configured")
    print("2. ✅ Real phone number added to Meta Developer Console")
    print("3. ✅ Production access granted")
    print("4. ✅ Environment variables set in cloud platform")
    print("5. ✅ Webhook URL updated in Meta Developer Console")
    
    print("\n📱 Real WhatsApp Number Setup:")
    print("- Go to Meta Developer Console")
    print("- Add your real WhatsApp phone number")
    print("- Verify the phone number")
    print("- Get production access (may require business verification)")
    
    print("\n☁️ Cloud Deployment:")
    print("- Railway: https://railway.app")
    print("- Render: https://render.com")
    print("- Set environment variables in cloud dashboard")
    print("- Update webhook URL to: https://your-app.railway.app/webhook")

if __name__ == "__main__":
    setup_production_env()
