# Emotion Detection Web App

## Overview
This web application uses deep learning to detect emotions from images and live video captures. It's built with Flask and TensorFlow, providing real-time emotion detection capabilities.

## Features
- Image upload for emotion detection
- Live video capture for real-time emotion detection
- User tracking and history
- Responsive web interface
- SQLite database integration

## Technical Stack
- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- ML Framework: TensorFlow
- Image Processing: OpenCV
- Database: SQLite

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Access the application:
Open your web browser and navigate to `http://localhost:5000`

## Project Structure
```
IDOWU_23CD034333_EMOTION_DETECTION_WEB_APP/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/
│   └── index.html
├── app.py
├── model.py
├── requirements.txt
└── README.md
```

## Database Schema
The application uses SQLite with the following schema:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    image_path TEXT,
    emotion TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Deployment
The application is hosted on render.com. Visit [link_to_my_web_app.txt](link_to_my_web_app.txt) for the live version.