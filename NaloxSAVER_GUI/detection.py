import cv2
import mediapipe as mp
import numpy as np
import time
from person import Person, get_person_id
from gpio_control import blink_led, set_servo_angle
# from app import get_socketio

# socketio = get_socketio()


mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=5, min_detection_confidence=0.5)

persons = []
next_person_id = 0

zoom_factor = 0.4
offset_y_inches = -0.2
offset_x_inches = 0.8
dpi = 30
offset_y_pixels = int(offset_y_inches * dpi)
offset_x_pixels = int(offset_x_inches * dpi)

def crop_above(frame, zoom_factor, offset_y_pixels, offset_x_pixels):

    height, width = frame.shape[:2]
    new_height, new_width = int(height / zoom_factor), int(width / zoom_factor)
    
    # Adjust the starting row to account for the vertical offset due to camera position
    start_row = int((height - new_height) / 2) - offset_y_pixels
    start_row = max(0, start_row)  
    end_row = start_row + new_height
    if end_row > height:
        end_row = height
        start_row = height - new_height

    # Adjust the starting column to account for the horizontal offset
    start_col = int((width - new_width) / 2) - offset_x_pixels
    start_col = max(0, start_col)  
    end_col = start_col + new_width
    if end_col > width:
        end_col = width
        start_col = width - new_width

    return frame[start_row:end_row, start_col:end_col]

def pixel_to_temperature(pixel_value, min_temp=20, max_temp=100):
    return min_temp + (pixel_value / 255) * (max_temp - min_temp)

# def process_frame(regular_frame, thermal_frame):
#     global next_person_id, persons, last_extraction_time
#     current_time = time.time()

#     # Crop the regular camera frame with vertical and horizontal offsets
#     cropped_frame = crop_above(regular_frame, zoom_factor, offset_y_pixels, offset_x_pixels) 
#     thermal_height, thermal_width = thermal_frame.shape[:2]
#     zoomed_frame_resized = cv2.resize(cropped_frame, (thermal_width, thermal_height))

    
#     if current_time - last_extraction_time >= 1:
#             last_extraction_time = current_time

#             rgb_frame = cv2.cvtColor(zoomed_frame_resized, cv2.COLOR_BGR2RGB)
#             results = face_detection.process(rgb_frame)

#             if results.detections:
#                 for detection in results.detections:
#                     bboxC = detection.location_data.relative_bounding_box
#                     ih, iw, _ = rgb_frame.shape
#                     x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
#                     person_id = get_person_id((x, y, w, h))
                   
#                     if person_id is None:
#                         person_id = next_person_id
#                         persons.append(Person(person_id, (x, y, w, h)))
#                         next_person_id += 1
                    
#                     person = [p for p in persons if p.id == person_id][0]
#                     person.update_bbox((x, y, w, h))

#                     face_results = face_mesh.process(rgb_frame)
                    
#                     if face_results.multi_face_landmarks:
#                         for face_landmarks in face_results.multi_face_landmarks:
#                             nose_tip = face_landmarks.landmark[1]
#                             nose_center_x = int(nose_tip.x * iw)
#                             nose_center_y = int(nose_tip.y * ih)

#                             cv2.rectangle(zoomed_frame_resized, (x, y), (x + w, y + h), (255, 0, 0), 2)
#                             cv2.circle(zoomed_frame_resized, (nose_center_x, nose_center_y), 5, (0, 0, 255), -1)

#                             if len(thermal_frame.shape) == 3 and thermal_frame.shape[2] == 3:
#                                 thermal_frame_gray = cv2.cvtColor(thermal_frame, cv2.COLOR_BGR2GRAY)
#                             else:
#                                 thermal_frame_gray = thermal_frame

#                             nose_temperature_pixel_value = thermal_frame_gray[nose_center_y, nose_center_x]
#                             nose_temperature = pixel_to_temperature(nose_temperature_pixel_value, min_temp=17.2, max_temp=33.4)

#                             person.add_temperature(nose_temperature)
#                             if person.check_death():
                                
                                
#                                 socketio.emit('death_detected', {'person_id': person_id}, namespace='/')
#                                 persons = [] 
#                                 next_person_id = 0
                                
#                                 blink_led()
#                                 # Move servo to indicate detection
#                                 set_servo_angle(90)  # Adjust angle as needed

                                

#                             print(f'Temperature at nose for person {person_id}: {nose_temperature:.2f} °C')
#                             cv2.putText(zoomed_frame_resized, f'{nose_temperature:.2f} °C', (nose_center_x, nose_center_y - 10),
#                                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                            
                

#         persons = [person for person in persons if current_time - person.last_detected <= 10]

#     return zoomed_frame_resized  # 返回处理后的视频帧
