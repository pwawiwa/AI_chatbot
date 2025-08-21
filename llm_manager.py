# llm_manager.py

import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_llm_response(messages, prices_data, model="gpt-4o-mini", temperature=0.7):
    """Generates a response from the LLM based on the given conversation history.
    """
    system_message = f"""Anda adalah seorang asisten bot WhatsApp untuk klinik kecantikan Almeera. 
Ini adalah daftar perawatan yang tersedia beserta deskripsi dan harganya: {prices_data}.

Anda harus merespons dalam Bahasa Indonesia dengan gaya yang girly, casual, dan elegan.
Ketika pasien menjelaskan keluhan kulit atau mencari perawatan, analisis keluhan mereka dengan cermat.
Kemudian, rekomendasikan perawatan atau paket perawatan yang paling sesuai dari daftar yang diberikan.
Jelaskan perawatan yang direkomendasikan secara detail, termasuk nama perawatan, deskripsi, dan harga.
Jika pasien menanyakan tentang perawatan tertentu, berikan penjelasan lengkap tentang perawatan tersebut (nama, deskripsi, harga, dan untuk apa perawatan itu terbaik).
Jika keluhan pasien tidak mengindikasikan tindakan spesifik, berikan informasi umum mengenai perawatan kulit atau sarankan konsultasi lebih lanjut.
Jaga agar respons Anda tetap ringkas, antara 3 hingga 5 kalimat, kecuali jika detail perawatan lengkap diminta.
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message}
            ] + messages, # Append user messages after system message
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting LLM response: {e}")
        return "Maaf, minra lagi tidak dapat memproses permintaan kamu saat ini." # Updated error message in Bahasa Indonesia

def moderate_content(text):
    """Checks content for moderation issues using OpenAI's moderation API."""
    try:
        response = client.moderations.create(input=text)
        moderation_output = response.results[0]
        if moderation_output.flagged:
            print("Content flagged by moderation API.")
            return True, moderation_output.categories.model_dump_json(indent=2)
        else:
            return False, "Content is clean."
    except Exception as e:
        print(f"Error during content moderation: {e}")
        return False, "Moderation service unavailable."