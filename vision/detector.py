import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class FaceDetector:
    def __init__(
        self,
        model_path="models/blaze_face_short_range.tflite",
        min_detection_confidence=0.6
    ):
        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.FaceDetectorOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            min_detection_confidence=min_detection_confidence
        )

        self.detector = vision.FaceDetector.create_from_options(options)

    def detect(self, frame):
        """
        Recebe um frame BGR do OpenCV.

        Retorna:
        [
            {
                "bbox": (x, y, w, h),
                "confidence": float
            }
        ]
        """

        # OpenCV trabalha em BGR.
        # MediaPipe espera RGB.
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Converte numpy array -> MediaPipe Image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Executa detecção
        result = self.detector.detect(mp_image)

        faces = []

        for detection in result.detections:

            bbox = detection.bounding_box

            x = bbox.origin_x
            y = bbox.origin_y
            w = bbox.width
            h = bbox.height

            # Evita coordenadas negativas
            x = max(0, x)
            y = max(0, y)

            # Limites da imagem
            frame_height, frame_width, _ = frame.shape

            w = min(w, frame_width - x)
            h = min(h, frame_height - y)

            # Confiança
            confidence = 0.0

            if detection.categories:
                confidence = detection.categories[0].score

            faces.append({
                "bbox": (x, y, w, h),
                "confidence": confidence
            })

        return faces

    def crop_face(self, frame, face, margin=0.20):

        x, y, w, h = face["bbox"]

        frame_height, frame_width = frame.shape[:2]

        margin_x = int(w * margin)
        margin_y = int(h * margin)

        x1 = max(0, x - margin_x)
        y1 = max(0, y - margin_y)

        x2 = min(frame_width, x + w + margin_x)
        y2 = min(frame_height, y + h + margin_y)

        cropped_face = frame[y1:y2, x1:x2]

        return cropped_face

    def close(self):
        self.detector.close()