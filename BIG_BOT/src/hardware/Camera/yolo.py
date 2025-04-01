from ultralytics import YOLO
import cv2
import math 

# Start webcam
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Load YOLO model
model = YOLO("yolov8n-oiv7.pt")  # Make sure this model supports the classes you need

# Confidence threshold
CONFIDENCE_THRESHOLD = 0.1  

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    # Process results
    for r in results:
        boxes = r.boxes
        for box in boxes:
            confidence = float(box.conf[0])  # Convert to float
            
            if confidence >= CONFIDENCE_THRESHOLD:  # Only display if confidence is high enough
                x1, y1, x2,  y2 = map(int, box.xyxy[0])  # Convert to int

                # Get class name
                cls = int(box.cls[0])
                class_name = model.names[cls]  # Get actual class name from YOLO model

                # Draw bounding box
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # Label text
                label = f"{class_name}: {confidence:.2f}"

                # Display text on screen
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
