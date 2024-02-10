import cv2
import mediapipe as mp
import time

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(1)
pTime = 0

jump_started = False
repetitions_count = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        point_25_y = results.pose_landmarks.landmark[25].y
        point_26_y = results.pose_landmarks.landmark[26].y
        point_29_y = results.pose_landmarks.landmark[29].y
        point_30_y = results.pose_landmarks.landmark[30].y
        point_13_y = results.pose_landmarks.landmark[13].y
        point_14_y = results.pose_landmarks.landmark[14].y
        point_15_y = results.pose_landmarks.landmark[15].y
        point_16_y = results.pose_landmarks.landmark[16].y

        if (
                (point_30_y < point_25_y or point_29_y < point_26_y) and
                (point_15_y < point_13_y and point_16_y < point_14_y) and
                not jump_started
        ):
            jump_started = True
            repetitions_count += 1
            print("Выполнен прыжок:", repetitions_count)
        elif point_30_y >= point_25_y and point_29_y >= point_26_y:
            jump_started = False

        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (int(cx), int(cy)), 10, (255, 0, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.putText(img, f"Jumps: {repetitions_count}", (70, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

    cv2.imshow('frame', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
