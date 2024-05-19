import cv2
import numpy as np
import os
from datetime import datetime


video_path = 'WhatsApp Video 2024-05-18 at 01.03.16_896fb8bb.mp4'
cap = cv2.VideoCapture(video_path)


if not cap.isOpened():
    print("Error: Could not open the video.")
    exit()


fire_threshold = 150  


output_folder = 'framesets'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


frame_index = 0

max_contour_area = 0
max_contour_coords = None

while True:
    ret, frame = cap.read()  
    if not ret:
        break 

    fire_mask = np.where(frame > fire_threshold, 255, 0).astype(np.uint8)# type: ignore

    fire_mask_gray = cv2.cvtColor(fire_mask, cv2.COLOR_BGR2GRAY)

    filtered_mask = cv2.medianBlur(fire_mask_gray, 5)  

    contours, _ = cv2.findContours(filtered_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        output_path = os.path.join(output_folder, timestamp + '.jpg')
        cv2.imwrite(output_path, frame)
        print(f"Saved frame {frame_index} with fire detection to {output_path}")
        break

    frame_index += 50


cap.release()
cv2.destroyAllWindows()
