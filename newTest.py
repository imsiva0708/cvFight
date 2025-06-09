import cv2
import mediapipe as mp

# VideoPath = 'testAsset/boxingSrc.mp4'
VideoPath = 'testAsset/videoplayback.mp4'

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
cap = cv2.VideoCapture(VideoPath)

selected_indices = [15, 16, 26, 12, 11]  # left/right wrist, right knee, left/right shoulders
hit_status = {
    15: False,  # left wrist
    16: False,  # right wrist
    26: False,  # right knee
    12: False,  # right shoulder
    11: False   # left shoulder
}

part_names = {
    15: "left_wrist",
    16: "right_wrist",
    26: "right_knee",
    12: "right_shoulder",
    11: "left_shoulder"
}

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    if not ret:
        break


    results = pose.process(frame)

    if results.pose_landmarks:
        h, w, _ = frame.shape

        landmark = results.pose_landmarks.landmark[0]
        x_head, y_head = int(landmark.x * w), int(landmark.y * h)

        landmark = results.pose_landmarks.landmark[25]
        x_left_knee, y_left_knee = int(landmark.x * w), int(landmark.y * h)

        cv2.circle(frame, (x_head, y_head), radius=30, color=(255, 0, 0), thickness=4)
        cv2.circle(frame, (x_left_knee, y_left_knee), radius=12, color=(255,0, 0 ), thickness=-1)

        bbox_top_left = (x_head + int(0.129*h),y_head+int(0.03*w))
        bbox_bottom_right = (x_head + int(0.49*h),y_left_knee+int(0.1*w))

        cv2.rectangle(frame,bbox_top_left,bbox_bottom_right,(255,0,0),4)

        for idx in selected_indices:
            landmark = results.pose_landmarks.landmark[idx]
            x = int(landmark.x * w)
            y = int(landmark.y * h)

            cv2.circle(frame, (x, y), radius=12, color=(0, 255, 0), thickness=-1)

            inside_box = (
                bbox_top_left[0] < x < bbox_bottom_right[0] and
                bbox_top_left[1] < y < bbox_bottom_right[1]
            )

            if inside_box and not hit_status[idx]:
                print(f"{part_names[idx]} HIT")
                hit_status[idx] = True  # mark as already hit

            elif not inside_box:
                hit_status[idx] = False  # reset if outside


    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
