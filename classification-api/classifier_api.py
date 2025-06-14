from flask import Flask, request, jsonify
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import os
import traceback
import pickle

# Initialize Flask app
app = Flask(__name__)
MAX_TOKEN_LENGTH = 512

# Load class mappings
try:
    with open('sentiment/mapped_classes.pkl', 'rb') as f:
        SENTIMENT_CLASSES = pickle.load(f)
    print("Successfully loaded sentiment class mapping")
except Exception as e:
    print(f"Error loading sentiment mapped_classes.pkl: {str(e)}")
    traceback.print_exc()
    raise

try:
    with open('subject/mapped_classes.pkl', 'rb') as f:
        SUBJECT_CLASSES = pickle.load(f)
    print("Successfully loaded subject class mapping")
except Exception as e:
    print(f"Error loading subject mapped_classes.pkl: {str(e)}")
    traceback.print_exc()
    raise

# Global variables for models and tokenizers
sentiment_model = None
sentiment_tokenizer = None
subject_model = None
subject_tokenizer = None

def initialize_sentiment_model():
    global sentiment_model, sentiment_tokenizer
    try:
        print("Trying to load local sentiment model and tokenizer...")
        sentiment_tokenizer = AutoTokenizer.from_pretrained('sentiment/Tokenizer')
        sentiment_model = AutoModelForSequenceClassification.from_pretrained('sentiment/Model')
        print("Successfully loaded local sentiment model and tokenizer")
    except Exception as e:
        print(f"Error loading local sentiment model: {str(e)}")
        traceback.print_exc()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device for sentiment model: {device}")
    sentiment_model.to(device)
    sentiment_model.eval()
    return device

def initialize_subject_model():
    global subject_model, subject_tokenizer
    try:
        print("Trying to load local subject model and tokenizer...")
        subject_tokenizer = AutoTokenizer.from_pretrained('subject/Tokenizer')
        subject_model = AutoModelForSequenceClassification.from_pretrained('subject/Model')
        print("Successfully loaded local subject model and tokenizer")
    except Exception as e:
        print(f"Error loading local subject model: {str(e)}")
        traceback.print_exc()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device for subject model: {device}")
    subject_model.to(device)
    subject_model.eval()
    return device


def classify_sentiment(text, Max_input_len=MAX_TOKEN_LENGTH):
    if sentiment_model is None or sentiment_tokenizer is None:
        raise ValueError("Sentiment model or tokenizer not initialized")
        
    encoded_text = sentiment_tokenizer.batch_encode_plus([text], padding=True, truncation=True, max_length=Max_input_len, return_tensors='pt')

    sentiment_model.eval()
    with torch.no_grad():
        input_ids = encoded_text['input_ids'].to(sentiment_device)
        attention_mask = encoded_text['attention_mask'].to(sentiment_device)

        outputs = sentiment_model(input_ids=input_ids, attention_mask=attention_mask)
        predictions = torch.argmax(outputs.logits, dim=1)
        return SENTIMENT_CLASSES.inverse_transform([predictions.item()])[0]


def classify_subject(text, Max_input_len=MAX_TOKEN_LENGTH):
    if subject_model is None or subject_tokenizer is None:
        raise ValueError("Subject model or tokenizer not initialized")
        
    encoded_text = subject_tokenizer.batch_encode_plus([text], padding=True, truncation=True, max_length=Max_input_len, return_tensors='pt')

    subject_model.eval()
    with torch.no_grad():
        input_ids = encoded_text['input_ids'].to(subject_device)
        attention_mask = encoded_text['attention_mask'].to(subject_device)

        outputs = subject_model(input_ids=input_ids, attention_mask=attention_mask)
        predictions = torch.argmax(outputs.logits, dim=1)
        prediction_idx = predictions.item()
        return SUBJECT_CLASSES[prediction_idx]

@app.route('/sentiment', methods=['POST'])
def sentiment():
    try:
        print("Received sentiment request")
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
        
        if 'text' not in data:
            print("Error: Missing text field")
            return jsonify({'error': 'Missing "text" field'}), 400

        text = data['text']
        print(f"Processing text for sentiment: {text}")
        sentiment_result = classify_sentiment(text)
        response = {'sentiment': sentiment_result}
        print(f"Sending sentiment response: {response}")
        return jsonify(response)
    except Exception as e:
        print(f"Error in sentiment endpoint: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/subject', methods=['POST'])
def subject():
    try:
        print("Received subject request")
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
        
        if 'text' not in data:
            print("Error: Missing text field")
            return jsonify({'error': 'Missing "text" field'}), 400

        text = data['text']
        print(f"Processing text for subject: {text}")
        subject_result = classify_subject(text)
        response = {'subject': subject_result}
        print(f"Sending subject response: {response}")
        return jsonify(response)
    except Exception as e:
        print(f"Error in subject endpoint: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("Starting Flask application...")
    # Initialize both models
    sentiment_device = initialize_sentiment_model()
    subject_device = initialize_subject_model()
    app.run(debug=True, port=5050, host='0.0.0.0') 