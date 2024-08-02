import cv2

def find_used_camera_indexes(num_attempts=10):
    """
    Find all the used camera indexes that can be opened.
    Returns a list of indexes that are currently in use.
    """
    used_indexes = []

    for idx in range(num_attempts):
        cap = cv2.VideoCapture(idx)
        # Check if the camera is opened and grab a frame
        if cap.isOpened():
            used_indexes.append(idx)
        cap.release()  # Release the camera object

    return used_indexes

# Example usage:
used_indexes = find_used_camera_indexes()

print(f"Used camera indexes: {used_indexes}")