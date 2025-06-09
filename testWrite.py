import os
import cv2

cap = cv2.VideoCapture('testAsset/boxingSrc.mp4')

ret = True
i = 0
while ret:
    ret, frame = cap.read()
    flipped_img = cv2.flip(frame,1)
    cv2.imwrite(f'frames/frame{i}.jpg',flipped_img)
    cv2.imshow(f'frame{i}',flipped_img)

    if cv2.waitKey(1) == ord('q'):
        break
    i+=1
# Cleanup
cap.release()
cv2.destroyAllWindows()
