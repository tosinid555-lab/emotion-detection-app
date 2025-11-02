import cv2
from model import EmotionDetector
import sys
import os

def test_emotion_detection(image_path):
    # Initialize the detector
    detector = EmotionDetector()
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"Error: File {image_path} does not exist")
        return
    
    # Read and display image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image {image_path}")
        return
    
    # Get emotion
    emotion = detector.predict(image_path)
    print(f"\nDetected emotion: {emotion}")
    
    # Display image with result
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, f"Emotion: {emotion}", (10, 30), font, 1, (0, 255, 0), 2)
    
    # Show the image
    cv2.imshow('Emotion Detection Test', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_emotion.py <path_to_image>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    test_emotion_detection(image_path)