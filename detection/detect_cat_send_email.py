from ultralytics import YOLO
import cv2
from datetime import datetime, timedelta
import requests
import time

last_send_time = datetime(2023, 10, 6, 12)

# URL of the endpoint
url = "http://localhost:8000/api/email/sendCat"
# Save the captured frame as an image file
image_filename = "captured_image.jpg"

# Load a model
model = YOLO("yolov8m.yaml")  # build a new model from scratch
model = YOLO("yolov8m.pt")  # load a pretrained model (recommended for training)

def capture_image():
    # Initialize the camera
    camera = cv2.VideoCapture(0)  # 0 represents the default camera (you can change it if you have multiple cameras)

    # Check if the camera is opened successfully
    if not camera.isOpened():
        print("Error: Could not open camera.")
        raise Exception("Could not open camera.")

    # Capture a frame from the camera
    ret, frame = camera.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Error: Could not read frame.")
        camera.release()  # Release the camera
        raise Exception("Could not read frame.")


    cv2.imwrite(image_filename, frame)

    # Release the camera
    camera.release()

    print(f"Image captured and saved as {image_filename}")


def detect_cat():
    global last_send_time
    results = model(image_filename)  # predict on an image
    if len(results) > 0:
        result = results[0]
        result_cls = [result.names[i] for i in result.boxes.cls.tolist()]

        if 'cat' in result_cls:
            current_time = datetime.now()
            print("[cat is here]", current_time)
            current_hour = datetime.now().hour
            time_difference = current_time - last_send_time
            
            print("[time_difference]: ", time_difference)
            
            if time_difference > timedelta(hours=1):
                if 7 <= current_hour and current_hour < 20:
                    try:
                        # Sending a POST request
                        response = requests.get(url)
                        last_send_time = datetime.now()
                        # Checking the response status code
                        if response.status_code == 200:
                            print("POST request sent successfully.")
                            print("[Email sent successfully]: ", last_send_time)
                            return
                        else:
                            print(f"Failed to send POST request. Status code: {response.status_code}")

                    except Exception as e:
                        print(f"An error occurred: {e}")
    else:
        print("[no cat]: ", datetime.now())

if __name__ == "__main__":
    while True:
        try:
            capture_image()
            detect_cat()
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(60)  # Wait for 60 seconds (1 minute) before running the function again
