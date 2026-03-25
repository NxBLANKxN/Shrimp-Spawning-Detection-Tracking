import cv2
import os
from concurrent.futures import ThreadPoolExecutor

video_path = r'C:\Users\NxBLANKxN\VS code file\蝦子辨識專題\videos\20260306.mov'
output_folder = r'C:\Users\NxBLANKxN\VS code file\蝦子辨識專題\image\20260306'
interval = 30  

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

cap = cv2.VideoCapture(video_path)
frame_id = 0
saved_id = 0

executor = ThreadPoolExecutor(max_workers=4)

def save_frame(frame, path):
    cv2.imwrite(path, frame)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_id % interval == 0:
        file_name = f"shrimp_{saved_id:04d}.jpg"
        path = os.path.join(output_folder, file_name)
        executor.submit(save_frame, frame.copy(), path)
        saved_id += 1

    frame_id += 1

cap.release()
executor.shutdown(wait=True)
print(f"抽樣完成！共儲存 {saved_id} 張圖片。")