import cv2
import time
# from detection import process_frame

from app import get_socketio
socketio = get_socketio()

from detection import crop_above, pixel_to_temperature


try:
    regular_cam = cv2.VideoCapture('/dev/video0')
    thermal_cam = cv2.VideoCapture('/dev/video2')
except Exception as e:
    print(f"Error initializing cameras: {e}")

# def generate_frames():
#     while True:
#         ret1, regular_frame = regular_cam.read()
#         ret2, thermal_frame = thermal_cam.read()

#         if not ret1 or not ret2:
#             print("Failed to capture frames")
#             continue

#         # processed_frame = process_frame(regular_frame, thermal_frame)
        
#         persons = [person for person in persons if current_time - person.last_detected <= 10]

        
#         ret, buffer = cv2.imencode('.jpg', processed_frame)
#         frame = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
def generate_frames():
    global last_extraction_time, flash_counter, persons, next_person_id
    while True:
        current_time = time.time()
        ret1, regular_frame = regular_cam.read()
        ret2, thermal_frame = thermal_cam.read()

        if not ret1 or not ret2:
            print("failaed to capture frames")
            break

        # Crop the regular camera frame with vertical and horizontal offsets
        zoomed_frame = crop_above(regular_frame, zoom_factor, offset_y_pixels, offset_x_pixels)
        
        # Resize the cropped frame to match the thermal frame size
        thermal_height, thermal_width = thermal_frame.shape[:2]
        zoomed_frame_resized = cv2.resize(zoomed_frame, (thermal_width, thermal_height))

        if current_time - last_extraction_time >= 1:
            last_extraction_time = current_time

            rgb_frame = cv2.cvtColor(zoomed_frame_resized, cv2.COLOR_BGR2RGB)
            results = face_detection.process(rgb_frame)

            if results.detections:
                for detection in results.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = rgb_frame.shape
                    x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                    person_id = get_person_id((x, y, w, h))
                   
                    if person_id is None:
                        person_id = next_person_id
                        persons.append(Person(person_id, (x, y, w, h)))
                        next_person_id += 1
                    
                    person = [p for p in persons if p.id == person_id][0]
                    person.update_bbox((x, y, w, h))

                    face_results = face_mesh.process(rgb_frame)
                    
                    if face_results.multi_face_landmarks:
                        for face_landmarks in face_results.multi_face_landmarks:
                            nose_tip = face_landmarks.landmark[1]
                            nose_center_x = int(nose_tip.x * iw)
                            nose_center_y = int(nose_tip.y * ih)

                            cv2.rectangle(zoomed_frame_resized, (x, y), (x + w, y + h), (255, 0, 0), 2)
                            cv2.circle(zoomed_frame_resized, (nose_center_x, nose_center_y), 5, (0, 0, 255), -1)

                            if len(thermal_frame.shape) == 3 and thermal_frame.shape[2] == 3:
                                thermal_frame_gray = cv2.cvtColor(thermal_frame, cv2.COLOR_BGR2GRAY)
                            else:
                                thermal_frame_gray = thermal_frame

                            nose_temperature_pixel_value = thermal_frame_gray[nose_center_y, nose_center_x]
                            nose_temperature = pixel_to_temperature(nose_temperature_pixel_value, min_temp=17.2, max_temp=33.4)

                            person.add_temperature(nose_temperature)
                            if person.check_death():
                                
                                
                                socketio.emit('death_detected', {'person_id': person_id}, namespace='/')
                                persons = [] 
                                next_person_id = 0
                                
                                blink_led()
                                # Move servo to indicate detection
                                set_servo_angle(90)  # Adjust angle as needed

                                

                            print(f'TemperaturÏe at nose for person {person_id}: {nose_temperature:.2f} °C')
                            cv2.putText(zoomed_frame_resized, f'{nose_temperature:.2f} °C', (nose_center_x, nose_center_y - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                            
                

        persons = [person for person in persons if current_time - person.last_detected <= 10]

        ret, buffer = cv2.imencode('.jpg', zoomed_frame_resized)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
     