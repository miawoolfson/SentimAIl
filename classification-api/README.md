# BERT Classification API

This Flask-based API provides two classification endpoints using BERT models:
1. Sentiment Analysis - Classifies text into sentiment categories
2. Subject Classification - Classifies text into business-related subject categories

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure your model files are in the correct directories:
   - Sentiment model: `sentiment/` directory
   - Subject model: `subject/` directory
   - Class mappings: `sentiment/mapped_classes.pkl` and `subject/mapped_classes.pkl`

3. Run the Flask application:
```bash
python app.py
```
The server will start on port 5000.

## API Endpoints

### 1. Sentiment Analysis
**Endpoint:** `/sentiment`  
**Method:** POST  
**Content-Type:** application/json  
**URL:** `http://localhost:5000/sentiment`

**Request Body:**
```json
{
    "text": "Your text here"
}
```

**Response:**
```json
{
    "sentiment": "sentiment_category"
}
```

### 2. Subject Classification
**Endpoint:** `/subject`  
**Method:** POST  
**Content-Type:** application/json  
**URL:** `http://localhost:5000/subject`

**Request Body:**
```json
{
    "text": "Your text here"
}
```

**Response:**
```json
{
    "subject": "subject_category"
}
```

## Usage Examples

### Using curl

1. Sentiment Analysis:
```bash
curl -X POST http://localhost:5000/sentiment \
     -H "Content-Type: application/json" \
     -d '{"text": "I am very happy with the service!"}'
```

2. Subject Classification:
```bash
curl -X POST http://localhost:5000/subject \
     -H "Content-Type: application/json" \
     -d '{"text": "Please schedule a meeting about the Q4 business strategy."}'
```

### Using Python requests

```python
import requests
import json

base_url = "http://localhost:5000"

# Sentiment analysis
sentiment_response = requests.post(
    f"{base_url}/sentiment",
    json={"text": "I am very happy with the service!"}
)
print("Sentiment:", sentiment_response.json())

# Subject classification
subject_response = requests.post(
    f"{base_url}/subject",
    json={"text": "Please schedule a meeting about the Q4 business strategy."}
)
print("Subject:", subject_response.json())
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 400 Bad Request: Missing or invalid JSON data
  ```json
  {
      "error": "No JSON data received"
  }
  ```
  or
  ```json
  {
      "error": "Missing \"text\" field"
  }
  ```

- 500 Internal Server Error: Server-side errors
  ```json
  {
      "error": "Internal server error"
  }
  ```

## Model Information

### Sentiment Model
- Location: `sentiment/` directory
- Class mappings: `sentiment/mapped_classes.pkl`

### Subject Model
- Location: `subject/` directory
- Class mappings: `subject/mapped_classes.pkl`
- Categories:
  - Company Business / Strategy
  - Document Collaboration
  - Employment
  - Logistics
  - Personal in Work Context

## Requirements
- Python 3.6+
- Flask 3.0.2
- PyTorch 2.2.1
- Transformers 4.38.2
- NumPy (<2.0.0)
- scikit-learn (>=1.0.0) 