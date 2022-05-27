import mediapipe as mp
import numpy as np


class FaceMeshDetector:
    def __init__(self, min_detection=0.5, min_tracking=0.5, debug=0):
        self.mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=min_detection,
            min_tracking_confidence=min_tracking
        )

        if debug > 0:
            self.drawing_spec = mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1)

        self.debug = debug

    def run(self, frame):
        res = self.mp_face_mesh.process(frame)

        if res.multi_face_landmarks is not None:
            if self.debug > 0:
                mp.solutions.drawing_utils.draw_landmarks(
                    image=frame,
                    landmark_list=res.multi_face_landmarks[0],
                    connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec = self.drawing_spec,
                    connection_drawing_spec = self.drawing_spec,
                )

            lmks = []
            norm_lmks = []
            for i, lmk in enumerate(res.multi_face_landmarks[0].landmark):
                # only add scaled head points without iris points
                if i < 468:
                    x, y = int(lmk.x * frame.shape[1]), int(lmk.y * frame.shape[0])
                    lmks.append((x, y))
                # add all points
                norm_lmks.append((lmk.x, lmk.y, lmk.z))

            return frame, np.array(lmks, dtype=np.float32), np.array(norm_lmks, dtype=np.float32)
        else:
            return frame, None, None
