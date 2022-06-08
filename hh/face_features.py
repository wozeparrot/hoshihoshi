import cv2
import numpy as np

from hh.utils import lerp, remap
from hh.face_model import ADJ_MODEL_INDICES, MODEL_POINTS


class FaceFeaturesCalculator:
    def __init__(self, frame_size, debug=0):
        self.head_rotation = np.zeros((3, 1))
        self.head_translation = np.zeros((3, 1))

        self.camera_matrix = np.array(
            [
                [frame_size[1], 0, frame_size[1] / 2],
                [0, frame_size[1], frame_size[0] / 2],
                [0, 0, 1],
            ],
            dtype=np.float64,
        )
        self.dist_co = np.zeros((4, 1), dtype=np.float32)

        self.debug = debug

    def head(self, frame, lmks, norm_lmks):
        face_2d = np.array([lmks[i] for i in ADJ_MODEL_INDICES], dtype=np.float32)

        _, self.head_rotation, self.head_translation = cv2.solvePnP(
            MODEL_POINTS,
            lmks,
            self.camera_matrix,
            self.dist_co,
            rvec=self.head_rotation,
            tvec=self.head_translation,
            useExtrinsicGuess=True,
            flags=cv2.SOLVEPNP_SQPNP,
        )

        rot_mat = cv2.Rodrigues(self.head_rotation)[0]
        pose_mat = cv2.hconcat((rot_mat, self.head_translation))
        euler = cv2.decomposeProjectionMatrix(pose_mat)[-1]

        if euler[0] < 0:
            euler[0] += 360
        euler[1] *= -1
        euler[2] *= -1

        return frame, euler, self.head_translation

    def mouth(self, frame, lmks, norm_lmks):
        m1 = norm_lmks[78]
        m2 = norm_lmks[81]
        m3 = norm_lmks[13]
        m4 = norm_lmks[311]
        m5 = norm_lmks[308]
        m6 = norm_lmks[402]
        m7 = norm_lmks[14]
        m8 = norm_lmks[178]

        mouth_aspect_ratio = np.clip(
            (
                np.linalg.norm(m2 - m8)
                + np.linalg.norm(m3 - m7)
                + np.linalg.norm(m4 - m6)
            )
            / (2 * np.linalg.norm(m1 - m5) + 1e-6),
            0.0,
            1.0,
        )

        left_eye_inner_corner = norm_lmks[133]
        left_eye_outer_corner = norm_lmks[130]
        right_eye_inner_corner = norm_lmks[362]
        right_eye_outer_corner = norm_lmks[263]

        eye_inner_corner_dist = np.linalg.norm(
            left_eye_inner_corner - right_eye_inner_corner
        )
        eye_outer_corner_dist = np.linalg.norm(
            left_eye_outer_corner - right_eye_outer_corner
        )

        upper_inner_lip = norm_lmks[13]
        lower_inner_lip = norm_lmks[14]
        left_mouth_corner = norm_lmks[61]
        right_mouth_corner = norm_lmks[291]

        raw_mouth_y_amt = np.linalg.norm(upper_inner_lip - lower_inner_lip)
        raw_mouth_x_amt = np.linalg.norm(left_mouth_corner - right_mouth_corner)

        raw_ratio_y = raw_mouth_y_amt / eye_inner_corner_dist
        raw_ratio_x = raw_mouth_x_amt / eye_outer_corner_dist

        ratio_y = remap((raw_ratio_y + mouth_aspect_ratio / 2.0), 0.17, 0.8)
        ratio_x = np.clip((remap(raw_ratio_x, 0.35, 0.9) - 0.4) * 2.2, -0.8, 0.8)

        return frame, (ratio_x, ratio_y)

    def eye(self, frame, lmks, norm_lmks):
        left_eye_inner_corner = norm_lmks[133]
        left_eye_outer_corner = norm_lmks[33]
        right_eye_inner_corner = norm_lmks[263]
        right_eye_outer_corner = norm_lmks[362]
        left_eye_lower = norm_lmks[159]
        left_eye_upper = norm_lmks[145]
        right_eye_lower = norm_lmks[386]
        right_eye_upper = norm_lmks[374]

        left_eye_width = np.linalg.norm(left_eye_inner_corner - left_eye_outer_corner)
        right_eye_width = np.linalg.norm(
            right_eye_inner_corner - right_eye_outer_corner
        )
        left_eye_height = np.linalg.norm(left_eye_upper - left_eye_lower)
        right_eye_height = np.linalg.norm(right_eye_upper - right_eye_lower)

        left_eye_mid = (
            left_eye_inner_corner + left_eye_outer_corner + left_eye_lower
        ) / 3.0
        right_eye_mid = (
            right_eye_inner_corner + right_eye_outer_corner + right_eye_lower
        ) / 3.0

        left_iris_center = norm_lmks[468]
        right_iris_center = norm_lmks[473]

        left_iris_ratio_x = (left_iris_center[0] - left_eye_mid[0]) / (
            left_eye_width / 4.0
        )
        left_iris_ratio_x = np.clip(left_iris_ratio_x, -1.0, 1.0)
        left_iris_ratio_y = (left_iris_center[1] - left_eye_mid[1]) / (
            left_eye_height / 5.0
        )
        left_iris_ratio_y = np.clip(left_iris_ratio_y, -1.0, 1.0)

        right_iris_ratio_x = (right_iris_center[0] - right_eye_mid[0]) / (
            right_eye_width / 4.0
        )
        right_iris_ratio_x = np.clip(right_iris_ratio_x, -1.0, 1.0)
        right_iris_ratio_y = (right_iris_center[1] - right_eye_mid[1]) / (
            right_eye_height / 5.0
        )
        right_iris_ratio_y = np.clip(right_iris_ratio_y, -1.0, 1.0)

        left_eye_ratio = left_eye_width / left_eye_height
        right_eye_ratio = right_eye_width / right_eye_height

        if left_eye_ratio > 3.2:
            left_iris_ratio_x = right_iris_ratio_x
            left_iris_ratio_y = right_iris_ratio_y
        elif right_eye_ratio > 3.2:
            right_iris_ratio_x = left_iris_ratio_x
            right_iris_ratio_y = left_iris_ratio_y
        elif left_eye_ratio > 3.2 and right_eye_ratio > 3.2:
            left_iris_ratio_x = 0.0
            left_iris_ratio_y = 0.0
            right_iris_ratio_x = 0.0
            right_iris_ratio_y = 0.0
        else:
            old_left_iris_ratio_x = left_iris_ratio_x
            old_left_iris_ratio_y = left_iris_ratio_y
            left_iris_ratio_x = lerp(0.2, left_iris_ratio_x, right_iris_ratio_x)
            left_iris_ratio_y = lerp(0.2, left_iris_ratio_y, right_iris_ratio_y)
            right_iris_ratio_x = lerp(0.2, right_iris_ratio_x, old_left_iris_ratio_x)
            right_iris_ratio_y = lerp(0.2, right_iris_ratio_y, old_left_iris_ratio_y)

        left_eye_ratio = 1.0 - remap(left_eye_ratio / 6, 0.52, 0.62)
        right_eye_ratio = 1.0 - remap(right_eye_ratio / 6, 0.52, 0.62)

        return (
            frame,
            (left_iris_ratio_x, left_iris_ratio_y),
            (right_iris_ratio_x, right_iris_ratio_y),
            (left_eye_ratio, right_eye_ratio),
        )
