import cv2
import numpy as np
import mediapipe as mp
import os
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
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    canvas = None
    draw_color = (0, 0, 255)
    brush_thickness = 8
    eraser_thickness = 50

    px, py = 0, 0
    os.makedirs("saved_drawings", exist_ok=True)

    print("=== AI 虛擬畫板啟動 ===")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape

        if canvas is None:
            canvas = np.zeros((h, w, 3), dtype=np.uint8)

        # 頂部選單 UI (紅, 綠, 藍, 黃, 橡皮擦)
        cv2.rectangle(frame, (20, 10), (160, 70), (0, 0, 255), -1)
        cv2.putText(frame, "RED", (60, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.rectangle(frame, (180, 10), (320, 70), (0, 255, 0), -1)
        cv2.putText(frame, "GREEN", (210, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.rectangle(frame, (340, 10), (480, 70), (255, 0, 0), -1)
        cv2.putText(frame, "BLUE", (380, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.rectangle(frame, (500, 10), (640, 70), (0, 255, 255), -1)
        cv2.putText(frame, "YELLOW", (530, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        cv2.rectangle(frame, (660, 10), (800, 70), (200, 200, 200), -1)
        cv2.putText(frame, "ERASER", (685, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        mode_text = "PAUSE"
        mode_color = (200, 200, 200)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                lm_list = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append((cx, cy))

                if len(lm_list) >= 21:
                    index_up = lm_list[8][1] < lm_list[6][1]
                    middle_up = lm_list[12][1] < lm_list[10][1]
                    ring_up = lm_list[16][1] < lm_list[14][1]
                    pinky_up = lm_list[20][1] < lm_list[18][1]

                    x1, y1 = lm_list[8]

                    # 握拳：清除畫布
                    if not index_up and not middle_up and not ring_up and not pinky_up:
                        canvas = np.zeros((h, w, 3), dtype=np.uint8)
                        mode_text = "CLEAR CANVAS"
                        mode_color = (0, 0, 255)
                        px, py = 0, 0

                    # 食指 + 中指：選擇模式 (停筆選色)
                    elif index_up and middle_up:
                        px, py = 0, 0
                        mode_text = "SELECTION / STOP"
                        mode_color = (255, 255, 0)
                        cv2.rectangle(frame, (x1 - 10, y1 - 10), (x1 + 10, y1 + 10), draw_color, -1)

                        if y1 < 70:
                            if 20 <= x1 <= 160:
                                draw_color = (0, 0, 255)
                            elif 180 <= x1 <= 320:
                                draw_color = (0, 255, 0)
                            elif 340 <= x1 <= 480:
                                draw_color = (255, 0, 0)
                            elif 500 <= x1 <= 640:
                                draw_color = (0, 255, 255)
                            elif 660 <= x1 <= 800:
                                draw_color = (0, 0, 0)

                    # 僅食指：繪圖模式
                    elif index_up and not middle_up:
                        mode_text = "DRAWING"
                        mode_color = (0, 255, 0)
                        cv2.circle(frame, (x1, y1), 10, draw_color, -1)

                        if px == 0 and py == 0:
                            px, py = x1, y1

                        current_thickness = eraser_thickness if draw_color == (0, 0, 0) else brush_thickness
                        cv2.line(canvas, (px, py), (x1, y1), draw_color, current_thickness)
                        px, py = x1, y1

        img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
        img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
        frame_bg = cv2.bitwise_and(frame, img_inv)
        frame_fg = cv2.bitwise_and(canvas, canvas)
        output_frame = cv2.add(frame_bg, frame_fg)

        cv2.putText(output_frame, f"STATUS: {mode_text}", (20, h - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, mode_color, 2)
        cv2.putText(output_frame, "[C] Clear | [S] Save | [Q] Quit", (w - 420, h - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("AI Virtual Drawing Board", output_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            canvas = np.zeros((h, w, 3), dtype=np.uint8)
        elif key == ord('s'):
            filename = f"saved_drawings/canvas_{int(time.time())}.png"
            cv2.imwrite(filename, canvas)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
