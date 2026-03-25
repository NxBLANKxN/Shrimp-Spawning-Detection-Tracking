import cv2
from ultralytics import YOLO
from collections import defaultdict

# ===== 模型 =====
model = YOLO(r'model\best20260316_5.pt')

# ===== 影片 =====
video_path = r'videos\20260307.mov'
cap = cv2.VideoCapture(video_path)

# ===== 視窗 =====
cv2.namedWindow("Shrimp_Detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Shrimp_Detection", 1280, 800)

paused = False

# ===== 儲存軌跡 =====
track_history = defaultdict(list)

print("操作說明：")
print("  - 按 [空白鍵]：暫停 / 繼續")
print("  - 按 [Q] 鍵：退出程式")

while cap.isOpened():

    if not paused:
        success, frame = cap.read()

        if not success:
            print("影片播放結束或讀取失敗")
            break

        # ===== YOLO 追蹤 =====
        results = model.track(
            frame,
            conf=0.3,
            imgsz=640,
            iou=0.35,
            device=0,
            tracker=r"C:\Users\NxBLANKxN\VS code file\蝦子辨識專題\bytetrack.yaml",
            persist=True,
            verbose=False
        )

        annotated_frame = frame.copy()

        for r in results:

            boxes = r.boxes

            if boxes.id is not None:

                ids = boxes.id.cpu().numpy()
                xyxy = boxes.xyxy.cpu().numpy()

                shrimp_count = len(ids)

                for box, track_id in zip(xyxy, ids):

                    x1, y1, x2, y2 = map(int, box)
                    track_id = int(track_id)

                    # ===== 畫框 =====
                    cv2.rectangle(
                        annotated_frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    # ===== 顯示 ID =====
                    cv2.putText(
                        annotated_frame,
                        f"ID {track_id}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

                    # ===== 中心點 =====
                    cx = int((x1 + x2) / 2)
                    cy = int((y1 + y2) / 2)

                    # ===== 儲存軌跡 =====
                    track = track_history[track_id]
                    track.append((cx, cy))

                    if len(track) > 50:
                        track.pop(0)

                    # ===== 畫軌跡 =====
                    for i in range(1, len(track)):
                        cv2.line(
                            annotated_frame,
                            track[i - 1],
                            track[i],
                            (0, 255, 255),
                            2
                        )

                # ===== 顯示蝦數量 =====
                cv2.putText(
                    annotated_frame,
                    f"Shrimp Count: {shrimp_count}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

        cv2.imshow("Shrimp_Detection", annotated_frame)

    # ===== 鍵盤控制 =====
    key = cv2.waitKey(1) & 0xFF

    if key == ord(' '):
        paused = not paused
        status = "暫停" if paused else "繼續"
        print(f"目前狀態：{status}")

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()