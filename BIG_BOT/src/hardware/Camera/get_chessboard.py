import cv2
import time
import os

def capture_screenshots(output_folder="screenshots", interval=1):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(1,  cv2.CAP_DSHOW)  # Open default camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    try:
        count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break
            
            # Display the frame
            cv2.imshow("Camera Feed", frame)
            
            filename = os.path.join(output_folder, f"screenshot_{count}.png")
            cv2.imwrite(filename, frame)
            print(f"Saved: {filename}")
            count += 1
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            time.sleep(interval)  # Wait for specified interval
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_screenshots()
