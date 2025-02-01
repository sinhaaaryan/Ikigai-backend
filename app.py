from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Server is running"
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        from openai import OpenAI
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return jsonify({
                "status": "error",
                "message": "OpenAI API key not found"
            }), 500

        client = OpenAI(api_key=api_key)
        data = request.json
        
        # Test response without LLM call first
        return jsonify({
            "status": "success",
            "message": "API is working",
            "received_data": data
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "type": str(type(e))
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port) 