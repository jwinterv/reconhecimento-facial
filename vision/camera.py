import cv2


class Camera:
    def __init__(self, camera_index=0):
        self.capture = cv2.VideoCapture(camera_index)

        if not self.capture.isOpened():
            raise RuntimeError("Não foi possível acessar a câmera.")

    def read(self):
        success, frame = self.capture.read()

        if not success:
            return None

        return frame

    def release(self):
        if self.capture.isOpened():
            self.capture.release()