import sys
import threading
import time
import cv2
import dlib
import pyttsx3
import pygame
from scipy.spatial import distance as dist
from imutils import face_utils
import imutils

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QFont

# Initialize TTS
engine = pyttsx3.init()
engine.setProperty('rate', 160)
tts_speaking = False

# Initialize pygame
pygame.mixer.init()
beep_playing = False

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def _speak(text):
    global tts_speaking
    tts_speaking = True
    engine.say(text)
    engine.runAndWait()
    tts_speaking = False

def speak(text):
    global tts_speaking
    if not tts_speaking:
        threading.Thread(target=_speak, args=(text,), daemon=True).start()

def start_beep():
    global beep_playing
    if not beep_playing:
        beep_playing = True
        pygame.mixer.music.load("beep.mp3")
        pygame.mixer.music.play(-1)

def stop_beep():
    global beep_playing
    if beep_playing:
        pygame.mixer.music.stop()
        beep_playing = False

# Detection Thread
class DrowsinessThread(QThread):
    def run(self):
        shape_predictor_path = "shape_predictor_68_face_landmarks.dat"
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(shape_predictor_path)
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        EAR_THRESHOLD = 0.3
        EYE_CLOSED_SECONDS = 5
        NO_FACE_SECONDS = 7
        eye_closed_start = None
        no_face_start = None

        cap = cv2.VideoCapture("http://192.168.29.198:8080/video")  # Your IP cam

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = imutils.resize(frame, width=400)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 0)

            if len(rects) == 0:
                if no_face_start is None:
                    no_face_start = time.time()
                elif time.time() - no_face_start > NO_FACE_SECONDS:
                    cv2.putText(frame, "Face not detected", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    speak("Please face the screen")
            else:
                no_face_start = None
                for rect in rects:
                    shape = predictor(gray, rect)
                    shape = face_utils.shape_to_np(shape)
                    leftEye = shape[lStart:lEnd]
                    rightEye = shape[rStart:rEnd]
                    leftEAR = eye_aspect_ratio(leftEye)
                    rightEAR = eye_aspect_ratio(rightEye)
                    ear = (leftEAR + rightEAR) / 2.0

                    if ear < EAR_THRESHOLD:
                        if eye_closed_start is None:
                            eye_closed_start = time.time()
                        elif time.time() - eye_closed_start >= EYE_CLOSED_SECONDS:
                            cv2.putText(frame, "Drowsiness Detected", (10, 60),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                            speak("Please wake up")
                            start_beep()
                    else:
                        eye_closed_start = None
                        stop_beep()

            cv2.imshow("Drowsiness Detector", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        stop_beep()

# PyQt5 GUI App
class DrowsinessApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Drowsiness Detector")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Drowsiness Detection System") 
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Create a bold, larger font
        button_font = QFont("Arial", 12, QFont.Bold)

        # Start Button
        self.start_btn = QPushButton("Start Detection", self)
        self.start_btn.clicked.connect(self.start_detection)
        self.start_btn.setFont(button_font)
        self.start_btn.setMinimumHeight(40)
        layout.addWidget(self.start_btn)

        # Exit Button
        self.exit_btn = QPushButton("Exit", self)
        self.exit_btn.clicked.connect(self.close)
        self.exit_btn.setFont(button_font)
        self.exit_btn.setMinimumHeight(40)
        layout.addWidget(self.exit_btn)

        self.setLayout(layout)

    def start_detection(self):
        self.thread = DrowsinessThread()
        self.thread.start()

# Launch App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DrowsinessApp()
    window.show()
    sys.exit(app.exec_())