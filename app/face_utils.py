import base64
import io
from typing import Optional, Tuple

import numpy as np
from PIL import Image
from deepface import DeepFace


_MODEL_CANDIDATES = [
    ("Facenet512", 0.35),
    ("ArcFace", 0.35),
    ("VGG-Face", 0.4),
]
_DETECTOR_CANDIDATES = [
    "mediapipe",
    "retinaface",
    "opencv",
    "mtcnn",
    "ssd",
]


def _image_from_base64(data_uri: str) -> Image.Image:
    header, b64data = data_uri.split(",", 1) if "," in data_uri else ("", data_uri)
    img_bytes = base64.b64decode(b64data)
    return Image.open(io.BytesIO(img_bytes)).convert("RGB")


def get_face_embedding_from_base64(data_uri: str) -> Optional[list[float]]:
    image = _image_from_base64(data_uri)
    np_img = np.array(image)

    for detector in _DETECTOR_CANDIDATES:
        for model_name, _ in _MODEL_CANDIDATES:
            try:
                reps = DeepFace.represent(
                    img_path=np_img,
                    model_name=model_name,
                    detector_backend=detector,
                    enforce_detection=True,
                    align=True,
                )
                if isinstance(reps, list) and reps:
                    vector = reps[0]["embedding"]
                    return [float(v) for v in vector]
            except Exception:
                continue

    return None


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def match_face(embedding: list[float], stored_embedding: list[float], threshold: float | None = None) -> Tuple[bool, float]:
    a = np.asarray(embedding, dtype=np.float32)
    b = np.asarray(stored_embedding, dtype=np.float32)
    score = cosine_similarity(a, b)

    if threshold is None:
        dim = len(embedding)
        threshold = 0.35 if dim <= 1024 else 0.4

    return score >= float(threshold), score
