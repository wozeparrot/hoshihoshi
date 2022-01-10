# python stdlib imports
from argparse import ArgumentParser
from multiprocessing import Process, Queue
import queue
import threading
import time
import signal
import sys
import math
from typing import Tuple
import json

# 3rd party imports
import cv2
from hh.utils import eprint
import numpy as np
from websocket_server import WebsocketServer as WSServer

# import our own stuff
import hh.face_mesh
import hh.face_features
from hh.smoother import SmootherKF, SmootherDEMA, SmootherTEMA


# --- CONFIG ---
DEBUG = 1


# --- MAIN ---
# thread event to stop all threads
stop_all = threading.Event()


class ThreadedCapture(Process):
    def __init__(self, q: Queue, src=0, width=640, height=480):
        super(ThreadedCapture, self).__init__()

        self.q = q

        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.killed = False
    
    def stop(self):
        self.killed = True
    
    def run(self):
        while not self.killed:
            start_time = time.time()

            g, f = self.cap.read()
            if g:
                try:
                    self.q.put_nowait((f, start_time))
                except queue.Full:
                    continue

        self.cap.release()


class ThreadedOutput(Process):
    def __init__(self, q: Queue):
        super(ThreadedOutput, self).__init__()

        self.q = q

        self.killed = False
    
    def stop(self):
        self.killed = True
    
    def run(self):
        server = WSServer(host="0.0.0.0", port=6789)
        server.run_forever(threaded=True)

        clients = []
        def ws_new_client(client, server):
            clients.append(client)
        server.set_fn_new_client(ws_new_client)
        def ws_message(client, server, message):
            if len(clients) >= 2:
                for i in range(1, len(clients)):
                    server.send_message(clients[i], message)
        server.set_fn_message_received(ws_message)

        while not self.killed:
            f = self.q.get()
            if len(clients) > 0:
                server.send_message(clients[0], json.dumps(f[2]))
            
            b, jpeg = cv2.imencode(".jpg", f[0])
            if not b:
                continue

            sys.stdout.buffer.write(jpeg.tobytes())


class ThreadedProcessing(Process):
    def __init__(self, iq: Queue, oq: Queue, frame_size: Tuple=(640, 480), head_rotation_offsets=(0, 0, 0)):
        super(ThreadedProcessing, self).__init__()

        self.iq = iq
        self.oq = oq

        self.head_rotation_offsets = head_rotation_offsets

        # self.face_mesh = hh.face_mesh.FaceMeshDetector(debug=DEBUG) # for some reason doesn't work if initialized here
        self.face_features = hh.face_features.FaceFeaturesCalculator(frame_size, debug=DEBUG)
        
        self.head_rotation_smoothers = [SmootherTEMA(0.1) for i in range(3)]
        self.head_translation_smoothers = [SmootherTEMA(0.1) for i in range(3)]
        self.mouth_ratio_smoothers = [SmootherKF() for i in range(2)]
        self.left_iris_ratio_smoothers = [SmootherTEMA(0.04) for i in range(2)]
        self.right_iris_ratio_smoothers = [SmootherTEMA(0.04) for i in range(2)]
        self.eye_ratio_smoothers = [SmootherTEMA(0.1) for i in range(2)]

        self.head_rotation = np.zeros((3, 1))
        self.head_translation = np.zeros((3, 1))
        self.mouth_ratio = np.zeros((2, 1))
        self.left_iris_ratio = np.zeros((2, 1))
        self.right_iris_ratio = np.zeros((2, 1))
        self.eye_ratios = np.zeros((2, 1))
        
        self.time_smoother = SmootherKF()

        self.camera_matrix = np.array(
            [[frame_size[1], 0, frame_size[1] / 2],
             [0, frame_size[1], frame_size[0] / 2],
             [0, 0, 1]], dtype=np.float64)
        self.dist_co = np.zeros((4, 1), dtype=np.float32)

        self.killed = False
    
    def stop(self):
        self.killed = True
    
    def run(self):
        self.face_mesh = hh.face_mesh.FaceMeshDetector(debug=DEBUG)

        while not self.killed:
            frame, start_time = self.iq.get()

            # get face landmarks
            frame.flags.writeable = False
            frame, lmks, norm_lmks = self.face_mesh.run(frame)

            # verify that there is a face
            if lmks is not None:
                # get head tracking data
                frame, raw_head_rotation, raw_head_translation = self.face_features.head(frame, lmks, norm_lmks)
                for i in range(3):
                    self.head_rotation_smoothers[i].update(raw_head_rotation[i])
                    self.head_rotation[i] = self.head_rotation_smoothers[i].state + self.head_rotation_offsets[i]
                    self.head_translation_smoothers[i].update(raw_head_translation[i])
                    self.head_translation[i] = self.head_translation_smoothers[i].state
                
                # get mouth tracking data
                frame, raw_mouth_ratio = self.face_features.mouth(frame, lmks, norm_lmks)
                for i in range(2):
                    self.mouth_ratio_smoothers[i].update(raw_mouth_ratio[i])
                    self.mouth_ratio[i] = self.mouth_ratio_smoothers[i].state

                # get iris tracking data
                frame, raw_left_iris_ratio, raw_right_iris_ratio, raw_eye_ratios = self.face_features.eye(frame, lmks, norm_lmks)
                for i in range(2):
                    self.left_iris_ratio_smoothers[i].update(raw_left_iris_ratio[i])
                    self.left_iris_ratio[i] = self.left_iris_ratio_smoothers[i].state
                    self.right_iris_ratio_smoothers[i].update(raw_right_iris_ratio[i])
                    self.right_iris_ratio[i] = self.right_iris_ratio_smoothers[i].state
                    self.eye_ratio_smoothers[i].update(raw_eye_ratios[i])
                    self.eye_ratios[i] = self.eye_ratio_smoothers[i].state

                if self.head_rotation[1] > 15:
                    self.right_iris_ratio = self.left_iris_ratio
                elif self.head_rotation[1] < -15:
                    self.left_iris_ratio = self.right_iris_ratio
                else:
                    old_left_iris_ratio = self.left_iris_ratio
                    self.left_iris_ratio = lerp(0.4, self.left_iris_ratio, self.right_iris_ratio)
                    self.right_iris_ratio = lerp(0.4, self.right_iris_ratio, old_left_iris_ratio)
                

                if DEBUG > 0:
                    # draw head pose axis
                    head_sin_pitch, head_sin_yaw, head_sin_roll = np.sin(np.deg2rad(self.head_rotation))
                    head_cos_pitch, head_cos_yaw, head_cos_roll = np.cos(np.deg2rad(self.head_rotation))
                    head_center = np.mean(lmks, axis=0).reshape((2, 1))
                    head_axis = np.array([
                        (head_cos_yaw * head_cos_roll, head_cos_pitch * head_sin_roll + head_cos_roll * head_sin_pitch * head_sin_yaw),
                        (-head_cos_yaw * head_sin_roll, head_cos_pitch * head_cos_roll - head_sin_pitch * head_sin_yaw * head_sin_roll),
                        (head_sin_yaw, -head_cos_yaw * head_sin_pitch)
                    ])
                    head_axis *= 80
                    head_axis += head_center
                    cv2.line(frame, (int(head_center[0]), int(head_center[1])), (int(head_axis[0][0]), int(head_axis[0][1])), (0, 0, 255), 3)
                    cv2.line(frame, (int(head_center[0]), int(head_center[1])), (int(head_axis[1][0]), int(head_axis[1][1])), (0, 255, 0), 3)
                    cv2.line(frame, (int(head_center[0]), int(head_center[1])), (int(head_axis[2][0]), int(head_axis[2][1])), (255, 0, 0), 3)

                    # draw iris circles
                    cv2.circle(frame, (int(self.left_iris_ratio[0] * (frame.shape[1] / 3)) + int(frame.shape[1] / 2), int(self.left_iris_ratio[1] * (frame.shape[0] / 3)) + int(frame.shape[0] / 2)), 4, (0, 0, 255), 2)
                    cv2.circle(frame, (int(self.right_iris_ratio[0] * (frame.shape[1] / 3)) + int(frame.shape[1] / 2), int(self.right_iris_ratio[1] * (frame.shape[0] / 3)) + int(frame.shape[0] / 2)), 4, (0, 255, 255), 2)

            try:
                self.oq.put_nowait((frame, start_time, {
                    "head_rotation": {
                        "x": float(self.head_rotation[0]),
                        "y": float(self.head_rotation[1]),
                        "z": float(self.head_rotation[2])
                    },
                    "head_translation": {
                        "x": float(self.head_translation[0]),
                        "y": float(self.head_translation[1]),
                        "z": float(self.head_translation[2])
                    },
                    "iris": {
                        "x": float((self.left_iris_ratio[0] + self.right_iris_ratio[0]) / 2.0),
                        "y": float((self.left_iris_ratio[1] + self.right_iris_ratio[1]) / 2.0) * -1.5
                    },
                    "eye": {
                        "left": float(self.eye_ratios[0]),
                        "right": float(self.eye_ratios[1])
                    },
                    "mouth": {
                        "x": float(self.mouth_ratio[0]),
                        "y": float(self.mouth_ratio[1]) * 2.0 - 1.0
                    }
                }))
            except queue.Full:
                continue

            if DEBUG > 1:
                self.time_smoother.update(time.time() - start_time)
                eprint(self.time_smoother.state)


def lerp(c, a, b):
    return ((1 - c) * a) + (c * b)


def main(args) -> None:
    cap_queue = Queue(4)
    cap = ThreadedCapture(cap_queue, args.camera)
    cap.start()

    out_queue = Queue(4)
    out = ThreadedOutput(out_queue)
    out.start()
    
    proc = ThreadedProcessing(cap_queue, out_queue,
        head_rotation_offsets=(12, 5, 0.12)
    )
    proc.start()

    stop_all.wait()

    out.terminate()
    proc.terminate()
    cap.terminate()


def signal_handler(sig, frame):
    stop_all.set()
signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--camera", type=int,
                        help="camera number",
                        default=0)

    main(parser.parse_args())