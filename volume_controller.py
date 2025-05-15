import cv2
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from gesture_detection import HandGestureDetector 

detector = HandGestureDetector()

# Audio setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()
min_vol, max_vol = vol_range[0], vol_range[1]

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    lm_list, img = detector.detect_hands(img)
    
    if lm_list:
        # Thumb tip = 4, Index tip = 8
        x1, y1 = lm_list[4][1], lm_list[4][2]
        x2, y2 = lm_list[8][1], lm_list[8][2]
        length = math.hypot(x2 - x1, y2 - y1)

        # Convert length to volume range
        vol = np.interp(length, [30, 200], [min_vol, max_vol])
        volBar = np.interp(length, [30, 200], [400, 150])
        volPercent = np.interp(length, [30, 200], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)

        # Draw volume bar
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 2)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPercent)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                    1, (0, 255, 0), 2)

        # Draw visual cues
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), -1)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), -1)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

    cv2.imshow("Volume Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()