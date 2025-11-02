import numpy as np
import cv2
from sklearn.ensemble import RandomForestClassifier
from PIL import Image

class EmotionDetector:
    def __init__(self):
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.classifier = RandomForestClassifier(n_estimators=100)
        self.is_trained = False
    
    def load_model(self):
        # Using OpenCV's built-in face detection
        if self.face_cascade.empty():
            raise ValueError("Error: Could not load face cascade classifier")
    
    def preprocess_image(self, image_path):
        # Load and preprocess the image for the model
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (48, 48))
        img = np.expand_dims(img, axis=-1)
        img = np.expand_dims(img, axis=0)
        img = img / 255.0
        return img
    
    def preprocess_image(self, image_path):
        """Preprocess the image for face detection"""
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not read image")
        return img

    def extract_features(self, face_roi):
        """Extract features from the face region"""
        # Resize to a fixed size
        face_roi = cv2.resize(face_roi, (48, 48))
        
        # Extract various features
        features = []
        
        # Basic statistical features
        features.extend([
            np.mean(face_roi),  # Average intensity
            np.std(face_roi),   # Standard deviation
            np.max(face_roi),   # Maximum intensity
            np.min(face_roi),   # Minimum intensity
        ])
        
        # Histogram features
        hist = cv2.calcHist([face_roi], [0], None, [32], [0, 256])
        features.extend(hist.flatten())
        
        # Edge features using Sobel
        sobel_x = cv2.Sobel(face_roi, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(face_roi, cv2.CV_64F, 0, 1, ksize=3)
        features.extend([
            np.mean(np.abs(sobel_x)),
            np.mean(np.abs(sobel_y))
        ])
        
        return np.array(features)

    def predict(self, image_path):
        try:
            # Read the image
            img = cv2.imread(image_path)
            if img is None:
                return 'error_reading_image'
                
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                return 'no_face_detected'
            
            # For the first face detected
            x, y, w, h = faces[0]
            face_roi = gray[y:y+h, x:x+w]
            
            # Extract features
            features = self.extract_features(face_roi)
            
            if not self.is_trained:
                # If model is not trained, use rule-based classification
                avg_intensity = np.mean(face_roi)
                std_intensity = np.std(face_roi)
                
                if std_intensity > 60:
                    return 'happy' if avg_intensity > 130 else 'angry'
                else:
                    return 'neutral' if avg_intensity > 130 else 'sad'
            
            # Make prediction using the trained model
            prediction = self.classifier.predict([features])[0]
            return self.emotions[prediction]
                    
        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            return 'error'