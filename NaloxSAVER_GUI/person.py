import time

class Person:
    def __init__(self, id, bbox):
        self.id = id
        self.bbox = bbox
        self.temperatures = []
        self.last_detected = time.time()
        self.alarm_on = False
        self.alarm_start_time = None
        self.previous_avg_temp = None
        self.death_detected_count = 0

    def update_bbox(self, bbox):
        self.bbox = bbox
        self.last_detected = time.time()

    def add_temperature(self, temp):
        self.temperatures.append(temp)
        if len(self.temperatures) > 5:
            self.temperatures.pop(0)

    def check_death(self):
        if len(self.temperatures) >= 2 and abs(self.temperatures[-2] - self.temperatures[-1]) <= 0.15:
            self.death_detected_count += 1
            if self.death_detected_count >= 6:
                self.death_detected_count = 0
                return True
        else:
            
            self.death_detected_count = 0 # Reset count if temperature data is incomplete
        return False

def get_person_id(bbox, persons):
    x, y, w, h = bbox
    for person in persons:
        px, py, pw, ph = person.bbox
        if abs(x - px) < 75 and abs(y - py) < 75:
            return person.id
    return None
