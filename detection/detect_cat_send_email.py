from ultralytics import YOLO
import cv2
from datetime import datetime, timedelta
import requests
import time
import os
import base64
from dmail import send_email, describe_cat_image
import requests

last_send_time = datetime(2023, 10, 6, 12)
detection_list = ['cat', 'dog', 'bear', 'teddy bear']
count = 0

# Save the captured frame as an image file
# image_filename = os.path.join("output", "captured_image.jpg")

# Load a model
#model = YOLO("yolov8m.yaml")  # build a new model from scratch
model = YOLO("yolov8x.pt")  # load a pretrained model (recommended for training)

def capture_image(image_filename):
    global count
    count += 1
    # Initialize the camera
    camera = cv2.VideoCapture(count % 2)  # 0 represents the default camera (you can change it if you have multiple cameras)
    camera.set(3, 960)
    camera.set(4, 540)
    # # Adjust camera lighting
    # for i in range(180):
    #     temp = camera.read()

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
    
def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def detect_cat(image_filename):
    global last_send_time
    # print("[detect_cat]: ")
    results = model(image_filename)  # predict on an image
    # print("[results]: ", results)
    if results and len(results) > 0:
        result = results[0]
        result_cls = [result.names[i] for i in result.boxes.cls.tolist()]

        print("result_cls: ", result_cls)

        if intersection(result_cls, detection_list):
            current_time = datetime.now()
            print("[cat is here]", current_time)
            current_hour = datetime.now().hour
            time_difference = current_time - last_send_time
            
            print("[time_difference]: ", time_difference)
            
            if time_difference > timedelta(hours=0.5):
                if 7 <= current_hour and current_hour < 20:
                    try:
                        with open(image_filename, "rb") as image_file:
                            # Convert the image to base64
                            image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

                        description = describe_cat_image(image_base64)
                        html_content = f'<div><p>{description}</p><img alt="My Image" src="data:image/jpeg;base64,{image_base64}"></div>'
                        
                        print("[description]: ", description)
                        send_email(html_content)
                        last_send_time = datetime.now()
                        print("[send email successful]: ", last_send_time)

                    except Exception as e:
                        print(f"[send email failed]: An error occurred: {e}")
        else:
            print("[no cat]: ", datetime.now())
            # remove image_filename
            os.remove(image_filename)
    else:
        print("[no cat]: ", datetime.now())
        # remove image_filename
        os.remove(image_filename)

if __name__ == "__main__":
    while True:
        try:
            # Get the current time
            current_time = datetime.now()
            # Format the time as a string with seconds
            time_string = current_time.strftime("%Y_%m_%d_%H_%M_%S")
            image_filename = os.path.join("output", time_string + ".jpg")
            capture_image(image_filename)
            detect_cat(image_filename)
        except Exception as e:
            print(f"An error occurred: {e}")

        print("Waiting for 30 seconds...")
        time.sleep(30)  # Wait for 60 seconds (1 minute) before running the function again
