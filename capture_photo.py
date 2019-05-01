import time
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
captured = False
time.sleep(1)
while(not captured):
    # Capture frame-by-frame
    ret, frame = cap.read()


    # Display the resulting frame
    cv2.imwrite('test.png',frame)
    break
    #captured = True
    #if (cv2.waitKey(1) & 0xFF == ord('q')) or captured:
    #    break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
