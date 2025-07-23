# import cv2
# import mediapipe as mp

# class HandDetector:
#     def __init__(self, 
#                  mode=False, 
#                  max_hands=2, 
#                  detection_confidence=0.7,
#                  tracking_confidence=0.7):
#         self.mode = mode
#         self.max_hands = max_hands

#         self.mp_hands = mp.solutions.hands
#         self.hands = self.mp_hands.Hands(
#             static_image_mode=self.mode,
#             max_num_hands=self.max_hands,
#             min_detection_confidence=detection_confidence,
#             min_tracking_confidence=tracking_confidence
#         )

#         self.mp_draw = mp.solutions.drawing_utils

#     def find_hands(self, frame, draw=True):
#         """
#         Detect hands and optionally draw landmarks.
#         """
#         img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         self.results = self.hands.process(img_rgb)

#         if self.results.multi_hand_landmarks and draw:
#             for handLms in self.results.multi_hand_landmarks:
#                 self.mp_draw.draw_landmarks(frame, handLms, self.mp_hands.HAND_CONNECTIONS)
#         return frame

#     def find_positions(self, frame, draw=True):
#         """
#         Return list of landmark positions for all hands.
#         Each hand's landmarks are returned as a list of dictionaries with id, x, y, z, and pressed state.
#         """
#         all_hands_landmarks = []

#         if self.results.multi_hand_landmarks:
#             for hand in self.results.multi_hand_landmarks:
#                 landmark_list = []
#                 h, w, _ = frame.shape
#                 for id, lm in enumerate(hand.landmark):
#                     cx, cy = int(lm.x * w), int(lm.y * h)
#                     landmark_list.append((id, cx, cy, lm.z))
#                     if draw:
#                         cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
#                 all_hands_landmarks.append(landmark_list)

#         return all_hands_landmarks

#     def is_pressing(self, landmarks):
#         """
#         Determine if a finger is pressing (e.g. tip below its pip joint).
#         This basic example uses index finger (id 8 tip, id 6 pip)
#         """
#         pressing_fingers = []
#         for finger_tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
#             tip_y = next((pt['y'] for pt in landmarks if pt['id'] == finger_tip), None)
#             pip_y = next((pt['y'] for pt in landmarks if pt['id'] == pip), None)
#             if tip_y is not None and pip_y is not None and tip_y > pip_y:
#                 pressing_fingers.append(finger_tip)
#         return pressing_fingers


import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, 
                 mode=False, 
                 max_hands=2, 
                 detection_confidence=0.7,
                 tracking_confidence=0.7):
        self.mode = mode
        self.max_hands = max_hands

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

        self.mp_draw = mp.solutions.drawing_utils
        self.mp_handedness = None
        self.results = None

    def find_hands(self, frame, draw=True):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks and draw:
            for handLms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, handLms, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def find_positions(self, frame, draw=True):
        """
        Return list of dicts: Each hand has 'landmarks' and 'type' (Left/Right)
        """
        hands_info = []

        if self.results.multi_hand_landmarks:
            for idx, hand in enumerate(self.results.multi_hand_landmarks):
                h, w, _ = frame.shape
                landmark_list = []
                for id, lm in enumerate(hand.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmark_list.append(( id, cx, cy, lm.z))
                    if draw:
                        cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

                # Determine if it's a left or right hand
                label = self.results.multi_handedness[idx].classification[0].label  # 'Left' or 'Right'
                hands_info.append((label, landmark_list))

        return hands_info

    def get_hand_palm_y(self, hand):
        """
        Return y-coordinate of palm base (landmark id 0) for the given hand
        """
        for pt in hand['landmarks']:
            if pt['id'] == 0:
                return pt['y']
        return None

    def is_pressing(self, landmarks):
        pressing_fingers = []
        for finger_tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
            tip_y = next((pt['y'] for pt in landmarks if pt['id'] == finger_tip), None)
            pip_y = next((pt['y'] for pt in landmarks if pt['id'] == pip), None)
            if tip_y is not None and pip_y is not None and tip_y > pip_y:
                pressing_fingers.append(finger_tip)
        return pressing_fingers
