# Medical Appointment Assistant - Web Interface

This is a web-based frontend for the Fine-tuned Gemini Medical Appointment Agent.

## Prerequisites

- Python 3.8+
- The dependencies listed in the root `requirements.txt` (including `flask` and `requests`).
- A `.env` file in the project root with the following variables:
  - `GOOGLE_CLOUD_PROJECT_ID`
  - `VERTEX_AI_REGION`
  - `VERTEX_AI_ENDPOINT_ID`
  - `GOOGLE_APPLICATION_CREDENTIALS_JSON`

## Setup

1. Navigate to the project root.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

Run the Flask application from the project root:

```bash
python web_app/app.py
```

Open your browser and go to: `http://127.0.0.1:5000`

## Structure

- `app.py`: Flask backend that interfaces with the `finetuned_model` package.
- `templates/index.html`: The chat interface HTML.
- `static/style.css`: Styles for the clean, medical-themed UI.
- `static/script.js`: Frontend logic for handling chat interactions.


