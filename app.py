from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        questions = data.get('questions', [])
        answers = data.get('answers', [])

        # Combine questions and answers
        qa_pairs = []
        for q, a in zip(questions, answers):
            qa_pairs.append(f"Question: {q}\nAnswer: {a}")
        
        combined_text = "\n\n".join(qa_pairs)

        # Create prompt for the LLM
        prompt = f"""Based on the following questions and answers, provide a personalized analysis 
        of the person's goals and aspirations, and offer specific advice for achieving them:

        {combined_text}

        Please provide a detailed response that includes:
        1. A summary of their aspirations
        2. Specific actionable steps they can take
        3. Potential challenges they might face and how to overcome them"""

        # Make OpenAI API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or your preferred model
            messages=[
                {"role": "system", "content": "You are a helpful career and personal development advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000
        )

        analysis = response.choices[0].message.content

        return jsonify({
            "status": "success",
            "analysis": analysis
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000))) 