import cv2
import mediapipe as mp
import time

def main():
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )

    cap = cv2.VideoCapture(0)
    last_gesture_time = time.time()
    cooldown = 1.2
    prev_x = None
    slide_page = 1
    total_slides = 10

    print("=== 手勢控制簡報系統 ===")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        status_msg = "Waiting for Gesture..."
        color = (255, 255, 255)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                palm_x = int(hand_landmarks.landmark[9].x * w)
                current_time = time.time()

                if prev_x is not None and (current_time - last_gesture_time > cooldown):
                    delta_x = palm_x - prev_x

                    if delta_x > 100:
                        if slide_page < total_slides:
                            slide_page += 1
                        status_msg = ">> NEXT SLIDE >>"
                        color = (0, 255, 0)
                        last_gesture_time = current_time
                    elif delta_x < -100:
                        if slide_page > 1:
                            slide_page -= 1
                        status_msg = "<< PREVIOUS SLIDE <<"
                        color = (0, 165, 255)
                        last_gesture_time = current_time

                prev_x = palm_x

        cv2.rectangle(frame, (50, 50), (w - 50, h - 100), (40, 40, 40), -1)
        cv2.rectangle(frame, (50, 50), (w - 50, h - 100), (255, 255, 255), 3)
        cv2.putText(frame, f"PRESENTATION SLIDE {slide_page} / {total_slides}", (w//2 - 220, h//2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

        cv2.putText(frame, f"Gesture Status: {status_msg}", (60, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Gesture Presentation Controller", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
