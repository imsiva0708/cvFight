import cv2
import mediapipe as mp

# VideoPath = 'testAsset/boxingSrc.mp4'
VideoPath = 'testAsset/videoplayback.mp4'

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
cap = cv2.VideoCapture(VideoPath)
# cap = cv2.VideoCapture(0)

selected_indices = [15, 16, 26, 12, 11]  # left/right wrist, right knee, left/right shoulders

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    if not ret:
        break

    # rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # results = pose.process(rgb_frame)
    results = pose.process(frame)

    if results.pose_landmarks:
        h, w, _ = frame.shape

        landmark = results.pose_landmarks.landmark[0]
        x_head, y_head = int(landmark.x * w), int(landmark.y * h)

        landmark = results.pose_landmarks.landmark[25]
        x_left_knee, y_left_knee = int(landmark.x * w), int(landmark.y * h)

        cv2.circle(frame, (x_head, y_head), radius=30, color=(255, 0, 0), thickness=4)
        cv2.circle(frame, (x_left_knee, y_left_knee), radius=12, color=(255,0, 0 ), thickness=-1)

        bbox_top_left = (x_head + int(0.129*h),y_head+int(0.05*w))
        bbox_bottom_right = (x_head + int(0.49*h),y_left_knee+int(0.1*w))

        cv2.rectangle(frame,bbox_top_left,bbox_bottom_right,(255,0,0),4)

        for idx in selected_indices:
            landmark = results.pose_landmarks.landmark[idx]
            x_px, y_px = int(landmark.x * w), int(landmark.y * h)
            cv2.circle(frame, (x_px, y_px), radius=12, color=(0, 255, 0), thickness=-1)

            if x_px > bbox_top_left[0] and y_px > bbox_top_left[1]:
                print('hit')

    # Show the frame
    cv2.imshow("Frame", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
