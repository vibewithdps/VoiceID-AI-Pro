import numpy as np


class Preprocessing:

    @staticmethod
    def pad_or_trim(vector, size):
        vector = np.asarray(vector)
        if len(vector) >= size:
            return vector[:size]
        padding = np.zeros(size - len(vector), dtype=vector.dtype)
        return np.concatenate([vector, padding])

    @staticmethod
    def normalize_matrix(matrix):
        matrix = np.asarray(matrix, dtype=np.float32)
        maximum = np.max(np.abs(matrix))
        return matrix if maximum == 0 else matrix / maximum
