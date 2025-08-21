#!/usr/bin/env python3
"""
Test langsung LLM untuk memastikan berfungsi
"""
from llm_manager import get_llm_response, moderate_content
from data_loader import load_prices_data

def test_llm_direct():
    """Test LLM secara langsung"""
    print("🧪 Testing LLM Directly...")
    
    # Load prices data
    prices = load_prices_data("Harga Agustus/prices_august.json")
    print(f"✅ Loaded {len(prices)} treatments")
    
    # Test moderation
    test_text = "Halo, mau treatment pico laser"
    flagged, reason = moderate_content(test_text)
    print(f"Moderation test: '{test_text}' -> Flagged: {flagged}, Reason: {reason}")
    
    # Test LLM response
    messages = [{"role": "user", "content": f"Pasien bertanya: {test_text}"}]
    print(f"\nSending to LLM: {test_text}")
    
    try:
        reply = get_llm_response(messages, prices)
        print(f"✅ LLM Response: {reply}")
    except Exception as e:
        print(f"❌ LLM Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_llm_direct()
