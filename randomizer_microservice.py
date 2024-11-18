from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/randomize', methods=['POST'])
def randomize_questions():
    try:
        # Parse the JSON payload from the request
        data = request.get_json()

        # Extract parameters
        num_questions = data.get("num_questions")
        total_questions = data.get("total_questions")
        previously_selected = data.get("previously_selected", [])

        # Input validation
        if not isinstance(num_questions, int) or not isinstance(total_questions, int):
            return jsonify({"error": "num_questions and total_questions must be integers."}), 400
        if num_questions > total_questions:
            return jsonify({"error": "Number of questions requested exceeds available questions."}), 400
        if not all(isinstance(q, int) for q in previously_selected):
            return jsonify({"error": "previously_selected must be a list of integers."}), 400

        # Create a pool of question numbers
        question_pool = list(range(1, total_questions + 1))

        # Remove previously selected questions and apply weights
        weights = []
        for q in question_pool:
            if q in previously_selected:
                weights.append(0.1)  # Lower weight for previously selected questions
            else:
                weights.append(1.0)  # Default weight

        # Select random questions with weighting
        selected_questions = random.choices(
            population=question_pool,
            weights=weights,
            k=num_questions
        )

        # Return the response as JSON
        return jsonify({"selected_questions": selected_questions}), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5025)