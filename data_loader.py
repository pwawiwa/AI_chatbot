# data_loader.py

import json

def load_prices_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"✅ Loaded {len(data)} treatments from {file_path}")
            return data
    except FileNotFoundError:
        print(f"⚠️  Warning: {file_path} not found, using empty list")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error decoding JSON from {file_path}: {e}")
        return []
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return []