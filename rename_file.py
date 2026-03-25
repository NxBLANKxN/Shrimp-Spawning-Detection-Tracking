import os
import sys

def rename_process():
    # 1. 使用者輸入資料夾路徑
    folder_path = r'C:\Users\NxBLANKxN\VS code file\蝦子辨識專題\image\20260307'
    
    # 檢查路徑是否存在
    if not os.path.isdir(folder_path):
        print(f"錯誤：找不到路徑 '{folder_path}'，請檢查路徑是否正確。")
        return

    # 2. 使用者輸入起始編號
    try:
        start_index = 47
    except ValueError:
        print("錯誤：起始編號必須是整數。")
        return

    # 取得檔案清單並排序
    files = os.listdir(folder_path)
    jpg_files = sorted([f for f in files if f.lower().endswith('.jpg')])

    if not jpg_files:
        print("該資料夾中沒有找到任何 .jpg 檔案。")
        return

    print(f"\n準備處理 {len(jpg_files)} 組檔案...\n")

    count = 0
    for old_jpg_name in jpg_files:
        base_name = os.path.splitext(old_jpg_name)[0]
        old_txt_name = base_name + ".txt"
        
        old_jpg_path = os.path.join(folder_path, old_jpg_name)
        old_txt_path = os.path.join(folder_path, old_txt_name)

        # 確保 txt 檔案存在才進行改名，避免破壞對應關係
        if os.path.exists(old_txt_path):
            new_number = str(start_index + count).zfill(4)
            new_base = f"shrimp_{new_number}"
            
            new_jpg_path = os.path.join(folder_path, new_base + ".jpg")
            new_txt_path = os.path.join(folder_path, new_base + ".txt")

            # 執行重新命名 (Rename)
            os.rename(old_jpg_path, new_jpg_path)
            os.rename(old_txt_path, new_txt_path)
            
            print(f"[{count+1}] {old_jpg_name} -> {new_base}.jpg")
            count += 1
        else:
            print(f"跳過：找不到 {old_jpg_name} 對應的 .txt 標註檔。")

    print(f"\n任務完成！共重新命名 {count} 組檔案。")

if __name__ == "__main__":
    rename_process()