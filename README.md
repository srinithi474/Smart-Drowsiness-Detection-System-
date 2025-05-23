# Smart Drowsiness Detection System using Python, OpenCV, dlib, and PyQt5

A real-time smart drowsiness detection system that alerts users when they are drowsy or inattentive. It uses facial landmarks to detect blinking and eye closure based on EAR (Eye Aspect Ratio) and includes a simple GUI built with PyQt5.

> **Note:** This is not a mobile or desktop app installer. You must run it from source using Python.

---

## **Table of Contents**
- [Features](#features)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Using IP Webcam](#using-ip-webcam)
- [Required Files & Downloads](#required-files--downloads)
- [How to Run](#how-to-run)
- [License](#license)

---

1. **Features**
- Real-time drowsiness detection using EAR
- Alerts via sound (beep) and text-to-speech
- Detects when face is not visible
- Clean PyQt5 GUI
- Works with laptop webcam or mobile IP webcam

---

2.**Requirements**
- Python 3.x
- OpenCV
- dlib
- PyQt5
- imutils
- scipy
- pyttsx3
- pygame

---

3.**Setup Instructions**

### 1. Install the dependencies:
```bash
-pip install opencv-python dlib pyttsx3 pygame imutils PyQt5 scipy

---

4.Using IP Webcam

-If your laptop doesn't have a webcam:
-Install IP Webcam app on your Android device.
-Connect your phone and laptop to the same Wi-Fi.
-Open the IP Webcam app, start the server, and it will show an IP like http://192.168.x.x:8080.
-In the code, replace this in cv2.VideoCapture():
-cap = cv2.VideoCapture("http://<your-ip>:8080/video")
-If you have a webcam, simply replace with:

cap = cv2.VideoCapture(0)

---

5. Required files and downloads:

- Download the shape predictor `.dat` file:  
  [Download shape_predictor_68_face_landmarks.dat](https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2)

  > After downloading, extract the `.dat` file and place it in your project directory.

- Download the beep alert sound file (or use your own named `beep.mp3`):  
  [Download beep.mp3](https://www.soundjay.com/button/beep-07.wav)

  > Rename it to `beep.mp3` if needed and put it in the same folder as your Python script.


6.How to Run

- Type python main2.py in your terminal
-Click Start Detection to begin and Exit to close the app. The app will alert you if:
-You close your eyes for more than 5 seconds
-Your face is not visible for more than 7 seconds

---

7.License

This project is licensed under the MIT License. See the LICENSE file for details.

---

8.Credits

Developed by Srinithi. Inspired by real-time computer vision applications in road safety.
