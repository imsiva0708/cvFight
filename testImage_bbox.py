import cv2
import mediapipe as mp
import matplotlib.pyplot as plt

TEST_IMG_PATH = 'frames/frame406.jpg'

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

image = cv2.imread(TEST_IMG_PATH)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

result = pose.process(image)
# print(result)
h,w,_ = image.shape
landmark = result.pose_landmarks.landmark[0]
# print(landmark)
print(h,w,_)
x_head = int(w*landmark.x)
y_head = int(h*landmark.y)

print(f'x:{x_head}, y:{y_head}')
image  = cv2.circle(image,(x_head,y_head),10,(255,0,0),-1)

landmark = result.pose_landmarks.landmark[25]
# print(landmark)
print(h,w,_)
x_leg = int(w*landmark.x)
y_leg = int(h*landmark.y)

print(f'Legs = x:{x_leg}, y:{y_leg}')
image = cv2.rectangle(image,(x_head + int(0.129*h),y_head+int(0.05*w)),(x_head + int(0.49*h),y_leg+int(0.1*w)),(255,0,0),4)

plt.imshow(image)
plt.show()
cv2.imshow('Window',image)
cv2.waitKey(0)
cv2.destroyAllWindows()