import cv2
import numpy as np
import tensorflow as tf


class FaceEmbedder:

    def __init__(self, model_path="models/mobilefacenet.tflite"):

        self.interpreter = tf.lite.Interpreter(
            model_path=model_path
        )

        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # Descobre automaticamente o tamanho esperado
        input_shape = self.input_details[0]["shape"]

        self.input_height = int(input_shape[1])
        self.input_width = int(input_shape[2])

        print("Modelo de embedding carregado")
        print("Input:", self.input_details[0]["shape"])
        print("Output:", self.output_details[0]["shape"])

    def preprocess(self, face):

        # BGR -> RGB
        face = cv2.cvtColor(
            face,
            cv2.COLOR_BGR2RGB
        )

        # Tamanho esperado pelo modelo
        face = cv2.resize(
            face,
            (self.input_width, self.input_height)
        )

        face = face.astype(np.float32)

        # Normalização típica do MobileFaceNet: [-1, 1]
        face = (face - 127.5) / 127.5

        # [H, W, 3] -> [1, H, W, 3]
        face = np.expand_dims(face, axis=0)

        return face

    def generate(self, face):

        input_data = self.preprocess(face)

        self.interpreter.set_tensor(
            self.input_details[0]["index"],
            input_data
        )

        self.interpreter.invoke()

        embedding = self.interpreter.get_tensor(
            self.output_details[0]["index"]
        )[0]

        # Normalização L2
        norm = np.linalg.norm(embedding)

        if norm > 0:
            embedding = embedding / norm

        return embedding