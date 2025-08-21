#!/usr/bin/env python3
"""
Simple test server untuk debug Railway deployment
"""
import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "Simple test server is running",
        "port": os.getenv("PORT", "8080")
    })

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"test": "success"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"🚀 Starting SIMPLE server on port {port}")
    print(f"📡 Server will be available at: http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
