from flask import Flask, render_template, request, jsonify
from model import EmotionDetector
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Initialize the emotion detector model
emotion_detector = EmotionDetector()

def init_db():
    conn = sqlite3.connect('emotion_detection.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  image_path TEXT,
                  emotion TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
        
        file = request.files['image']
        username = request.form.get('username', 'anonymous')
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        # Check file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if '.' not in file.filename or \
           file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save the image
        upload_folder = os.path.join(app.static_folder, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{username}_{timestamp}.jpg"
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Detect emotion
        emotion = emotion_detector.predict(filepath)
        
        # Store in database
        conn = sqlite3.connect('emotion_detection.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, image_path, emotion) VALUES (?, ?, ?)',
                 (username, filename, emotion))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'emotion': emotion,
            'image_path': filename
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)