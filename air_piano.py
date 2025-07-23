# import cv2
# import pygame
# import os
# import math
# from hand_detector import HandDetector  # Custom module (Mediapipe wrapper)

# # Initialize Pygame
# pygame.init()
# pygame.mixer.init()

# # Load sounds for 2 octaves (C4 to B5)
# note_names = [
#     "c4", "c#4", "d4", "d#4", "e4", "f4", "f#4", "g4", "g#4", "a4", "a#4", "b4",
#     "c5", "c#5", "d5", "d#5", "e5", "f5", "f#5", "g5", "g#5", "a5", "a#5", "b5"
# ]
# note_sounds = {note: pygame.mixer.Sound(f"sounds/{note}.ogg") for note in note_names}

# # Key layout
# white_notes = [n for n in note_names if "#" not in n]
# black_notes = [n for n in note_names if "#" in n]

# # Set camera and detector
# WIDTH, HEIGHT = 1280, 720
# cap = cv2.VideoCapture(0)
# detector = HandDetector(detection_confidence=0.7, max_hands=2)

# # Key layout constants
# radius_white = 40
# radius_black = 30
# offset_y_black = -25
# center_x = WIDTH // 2
# center_y = HEIGHT // 2 + 100
# spacing = 70  # horizontal spacing between keys

# # Generate key positions
# white_positions = []
# black_positions = {}

# for i, note in enumerate(white_notes):
#     x = center_x + (i - len(white_notes) // 2) * spacing
#     y = center_y
#     white_positions.append((note, (x, y)))

# for i, note in enumerate(black_notes):
#     base_note = note.replace("#", "")
#     try:
#         idx = white_notes.index(base_note)
#         x1 = white_positions[idx][1][0]
#         x2 = white_positions[idx + 1][1][0]
#         x = (x1 + x2) // 2
#         y = center_y + offset_y_black
#         black_positions[note] = (x, y)
#     except:
#         pass

# # State tracking
# playing_notes = set()
# volume = 1.0

# # Main loop
# while True:
#     success, frame = cap.read()
#     frame = cv2.resize(frame, (WIDTH, HEIGHT))
#     frame = cv2.flip(frame, 1)

#     hands = detector.find_hands(frame, draw=False)
#     lm_lists = detector.find_positions(frame)

#     overlay = frame.copy()

#     # Draw white keys
#     for note, pos in white_positions:
#         # cv2.circle(overlay, pos, radius_white, (255, 255, 255), -1)
#         # cv2.circle(overlay, pos, radius_white, (0, 0, 0), 2)
#         cv2.putText(overlay, note.upper(), (pos[0] - 20, pos[1] + 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

#     # Draw black keys
#     for note, pos in black_positions.items():
#         # cv2.circle(overlay, pos, radius_black, (0, 0, 0), -1)
#         cv2.putText(overlay, note.upper(), (pos[0] - 15, pos[1] + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


#     # Display volume bar always
#     vol_height = int(volume * 300)
#     cv2.rectangle(frame, (1150, HEIGHT - 350), (1190, HEIGHT - 50), (50, 50, 50), 2)
#     cv2.rectangle(frame, (1152, HEIGHT - 50 - vol_height), (1188, HEIGHT - 50), (0, 255, 0), -1)
#     cv2.putText(frame, f"{int(volume * 100)}%", (1150, HEIGHT - 360), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

#     # Blend overlay with frame
#     alpha = 0.4
#     cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

#     # Redraw hands
#     frame = detector.find_hands(frame, draw=True)

#     # Detect and play
#     if lm_lists:
#         for label, lmks in lm_lists:
#             if len(lmks) >= 21:
#                 index_tip = lmks[8][1:]
#                 index_pip = lmks[6][1:]
#                 thumb_tip = lmks[4][1:]
#                 palm_center = lmks[0][1:]

#                 # Volume control with right hand horizontal movement
#                 if label == "Right":  # thumb tip's x > mid means right hand (basic assumption)
#                     palm_y = palm_center[0]
#                     volume = max(0.2, min(1.0, palm_y / WIDTH))


#                 # Press detection
#                 is_pressed = index_tip[1] > index_pip[1]
#                 if is_pressed:
#                     note_played = None

#                     for note, pos in black_positions.items():
#                         if math.hypot(index_tip[0] - pos[0], index_tip[1] - pos[1]) < radius_black:
#                             note_played = note
#                             break
#                     if not note_played:
#                         for note, pos in white_positions:
#                             if math.hypot(index_tip[0] - pos[0], index_tip[1] - pos[1]) < radius_white:
#                                 note_played = note
#                                 break

#                     if note_played and note_played not in playing_notes:
#                         note_sounds[note_played].set_volume(volume)
#                         note_sounds[note_played].play()
#                         playing_notes.add(note_played)
#                         cv2.putText(frame, f"{note_played.upper()} {int(volume*100)}%", (50, 100 + 30 * len(playing_notes)),
#                                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#     # Update playing notes
#     new_playing = set()
#     if lm_lists:
#         for label, lmks in lm_lists:
#             if len(lmks) >= 9:
#                 index_tip = lmks[8][1:]
#                 index_pip = lmks[6][1:]
#                 if index_tip[1] > index_pip[1]:
#                     for note, pos in black_positions.items():
#                         if math.hypot(index_tip[0] - pos[0], index_tip[1] - pos[1]) < radius_black:
#                             new_playing.add(note)
#                     for note, pos in white_positions:
#                         if math.hypot(index_tip[0] - pos[0], index_tip[1] - pos[1]) < radius_white:
#                             new_playing.add(note)
#     playing_notes = playing_notes & new_playing

#     cv2.imshow("Air Piano - C4 to B5", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

import cv2
import pygame
import os
import math
from hand_detector import HandDetector  # Updated with MediaPipe Holistic

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load sounds for 2 octaves (C4 to B5)
note_names = [
    "c4", "c#4", "d4", "d#4", "e4", "f4", "f#4", "g4", "g#4", "a4", "a#4", "b4",
    "c5", "c#5", "d5", "d#5", "e5", "f5", "f#5", "g5", "g#5", "a5", "a#5", "b5"
]
note_sounds = {note: pygame.mixer.Sound(f"sounds/{note}.ogg") for note in note_names}

# Key layout
white_notes = [n for n in note_names if "#" not in n]
black_notes = [n for n in note_names if "#" in n]

# Set camera and detector
WIDTH, HEIGHT = 1280, 720
cap = cv2.VideoCapture(0)
detector = HandDetector(detection_confidence=0.7, max_hands=2)

# Key layout constants
radius_white = 40
radius_black = 30
offset_y_black = -25
center_x = WIDTH // 2
center_y = HEIGHT // 2 + 100
spacing = 70

# Generate key positions
white_positions = []
black_positions = {}

for i, note in enumerate(white_notes):
    x = center_x + (i - len(white_notes) // 2) * spacing
    y = center_y
    white_positions.append((note, (x, y)))

for i, note in enumerate(black_notes):
    base_note = note.replace("#", "")
    try:
        idx = white_notes.index(base_note)
        x1 = white_positions[idx][1][0]
        x2 = white_positions[idx + 1][1][0]
        x = (x1 + x2) // 2
        y = center_y + offset_y_black
        black_positions[note] = (x, y)
    except:
        pass

# State tracking
playing_notes = set()
volume = 1.0

# Main loop
while True:
    success, frame = cap.read()
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    frame = cv2.flip(frame, 1)

    hands = detector.find_hands(frame, draw=False)
    lm_lists = detector.find_positions(frame)

    overlay = frame.copy()

    # Draw white and black notes
    for note, pos in white_positions:
        cv2.putText(overlay, note.upper(), (pos[0] - 20, pos[1] + 7),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    for note, pos in black_positions.items():
        cv2.putText(overlay, note.upper(), (pos[0] - 15, pos[1] + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Display volume bar always
    vol_height = int(volume * 300)
    cv2.rectangle(frame, (1150, HEIGHT - 350), (1190, HEIGHT - 50), (50, 50, 50), 2)
    cv2.rectangle(frame, (1152, HEIGHT - 50 - vol_height), (1188, HEIGHT - 50), (0, 255, 0), -1)
    cv2.putText(frame, f"{int(volume * 100)}%", (1150, HEIGHT - 360),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Blend overlay
    alpha = 0.4
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # Redraw hand landmarks
    frame = detector.find_hands(frame, draw=True)

    if lm_lists:
        for label, lmks in lm_lists:
            if len(lmks) >= 21:
                palm_center = (lmks[0]['x'], lmks[0]['y'])

                # Volume control with right hand
                if label == "Left":
                    palm_y = palm_center[1]
                    volume = max(0.2, min(1.0, 1 - palm_y / HEIGHT))

                # Play notes only with left hand
                if label == "Right":
                    pressing_fingers = detector.is_pressing(lmks)
                    for tip_id in pressing_fingers:
                        tip = next((pt for pt in lmks if pt['id'] == tip_id), None)
                        if not tip:
                            continue
                        tip_x, tip_y = tip['x'], tip['y']

                        note_played = None
                        for note, pos in black_positions.items():
                            if math.hypot(tip_x - pos[0], tip_y - pos[1]) < radius_black:
                                note_played = note
                                break
                        if not note_played:
                            for note, pos in white_positions:
                                if math.hypot(tip_x - pos[0], tip_y - pos[1]) < radius_white:
                                    note_played = note
                                    break

                        if note_played and note_played not in playing_notes:
                            note_sounds[note_played].set_volume(volume)
                            note_sounds[note_played].play()
                            playing_notes.add(note_played)
                            cv2.putText(frame, f"{note_played.upper()} {int(volume*100)}%",
                                        (50, 100 + 30 * len(playing_notes)),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Update currently pressed notes
    new_playing = set()
    if lm_lists:
        for label, lmks in lm_lists:
            if label == "Left" and len(lmks) >= 21:
                pressing_fingers = detector.is_pressing(lmks)
                for tip_id in pressing_fingers:
                    tip = next((pt for pt in lmks if pt['id'] == tip_id), None)
                    if not tip:
                        continue
                    tip_x, tip_y = tip['x'], tip['y']
                    for note, pos in black_positions.items():
                        if math.hypot(tip_x - pos[0], tip_y - pos[1]) < radius_black:
                            new_playing.add(note)
                    for note, pos in white_positions:
                        if math.hypot(tip_x - pos[0], tip_y - pos[1]) < radius_white:
                            new_playing.add(note)
    playing_notes = playing_notes & new_playing

    cv2.imshow("Air Piano - C4 to B5", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
