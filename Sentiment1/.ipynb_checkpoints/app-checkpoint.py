from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Load the pre-trained model and label encoder
model = joblib.load('sentiment_model.pkl')
label_encoder = joblib.load('label_encoder.pkl')

def make_prediction(data):
    # Extract text from the incoming JSON data
    text = data.get('text', '')
    
    if not text:
        return {'error': 'No text provided for prediction'}, 400
    
    # Make prediction and get probabilities
    prediction = model.predict([text])
    prediction_proba = model.predict_proba([text])

    # Get the sentiment label
    sentiment = label_encoder.inverse_transform(prediction)[0]

    # Get the confidence score for the predicted class
    confidence = np.max(prediction_proba)  # Max probability for the predicted class

    # Return the result
    return {'sentiment': sentiment, 'confidence': confidence}, 200

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    print("Received data:", data)  # Log received data for debugging
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    result, status_code = make_prediction(data)
    return jsonify(result), status_code

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)