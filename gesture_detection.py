import cv2
import mediapipe as mp

class HandGestureDetector:
    def __init__(self, max_num_hands=2, detection_confidence=0.7, tracking_confidence=0.7):
        self.hands_module = mp.solutions.hands
        self.hands = self.hands_module.Hands(max_num_hands=max_num_hands,
                                             min_detection_confidence=detection_confidence,
                                             min_tracking_confidence=tracking_confidence)
        self.drawing_utils = mp.solutions.drawing_utils

    def detect_hands(self, image, draw=True):
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        hand_landmarks = []

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                if draw:
                    self.drawing_utils.draw_landmarks(image, handLms, self.hands_module.HAND_CONNECTIONS)
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    hand_landmarks.append((id, cx, cy))

        return hand_landmarks, image

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    detector = HandGestureDetector()

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        landmarks, frame = detector.detect_hands(frame)
        cv2.imshow("Hand Gesture Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
