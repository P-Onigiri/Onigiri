import cv2
import numpy as np
import os
from datetime import datetime
import requests

pushover_user_key = "uop8epposncmfq9quxkuhy63af1uoy"
pushover_api_token = "aztprr9exhjbm6wj85ru17i2kr1mqp"

def send_pushover_notification(title, message, image_path):
    url = "https://api.pushover.net/1/messages.json"
    files = {'attachment': open(image_path, 'rb')}
    data = {
        "token": pushover_api_token,
        "user": pushover_user_key,
        "title": title,
        "message": message
    }
    response = requests.post(url, data=data, files=files)
    return response

video_path = 'WhatsApp Video 2024-05-18 at 09.55.22_507c31fa.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open the video.")
    exit()

brightness_threshold = 150 

frame_index = 0

output_folder = 'frames_with_fire'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

while True:
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ret, frame = cap.read() 
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, bright_mask = cv2.threshold(gray_frame, brightness_threshold, 255, cv2.THRESH_BINARY)

    kernel = np.ones((5, 5), np.uint8)
    bright_mask = cv2.morphologyEx(bright_mask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(bright_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_contour_area = 0
    max_contour_coords = None

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        contour_area = cv2.contourArea(contour)

        if contour_area > max_contour_area:
            max_contour_area = contour_area
            max_contour_coords = (x, y, w, h)

    if max_contour_coords:
        x, y, w, h = max_contour_coords
        
        serenity_level = round((w * h) / 1000)  
        serenity_text = f"Serenity Level: {serenity_level}"
        cv2.putText(frame, serenity_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_path = os.path.join(output_folder, f'{timestamp}.jpg')
        cv2.imwrite(output_path, frame)
        print(f"Saved frame {frame_index} with fire detection to {output_path}")

        title = "Fire Detected!"
        message = f"Fire has been detected in the frame at {timestamp}. Please check the saved image."
        pushover_response = send_pushover_notification(title, message, output_path)
        print(f"Sent Pushover notification: {pushover_response.status_code}")


        break

    frame_index += 50 

cap.release()
cv2.destroyAllWindows()
