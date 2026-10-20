import numpy as np


class FaceRecognizer:

    def __init__(self, database, threshold=0.65):
        self.database = database
        self.threshold = threshold

    def cosine_similarity(self, embedding1, embedding2):

        embedding1 = embedding1 / np.linalg.norm(embedding1)
        embedding2 = embedding2 / np.linalg.norm(embedding2)

        return np.dot(
            embedding1,
            embedding2
        )

    def recognize(self, embedding):

        users = self.database.get_users()

        if not users:
            return None, 0.0

        best_user = None
        best_similarity = -1.0

        for user in users:

            similarity = self.cosine_similarity(
                embedding,
                user["embedding"]
            )

            if similarity > best_similarity:

                best_similarity = similarity
                best_user = user

        if best_similarity >= self.threshold:
            return best_user, best_similarity

        return None, best_similarity