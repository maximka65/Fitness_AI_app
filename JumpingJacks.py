import cv2
import mediapipe as mp
import time

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture("JumpingJacks.mov")
pTime = 0

jump_started = False
repetitions_count = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        # получаем координаты ключевых точек
        left_shoulder_y = results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].y
        left_hand_y = results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].y
        right_shoulder_y = results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].y
        right_hand_y = results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].y

        # проверяем условие для засчитывания прыжка
        if left_hand_y > left_shoulder_y and right_hand_y > right_shoulder_y and not jump_started:
            jump_started = True
            repetitions_count += 1
            print("Выполнен прыжок:", repetitions_count)
        elif left_hand_y <= left_shoulder_y and right_hand_y <= right_shoulder_y:
            jump_started = False

        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            cv2.circle(img, (int(cx), int(cy)), 10, (255, 0, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.putText(img, f"Jumping Jacks: {repetitions_count}", (70, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow('frame', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
