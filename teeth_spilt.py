import cv2
import numpy as np
import os
from skimage.morphology import remove_small_objects

# 路徑設置
desktop_path = './images/'# 資料庫位置
color_path= os.path.join(desktop_path, "color")                        # 彩色資料夾
bw_path = os.path.join(desktop_path, "bw")                             # 黑白牙齦資料夾
gum_path = os.path.join(desktop_path, "color", "gum")                  # 牙齦資料夾
teeth_path = os.path.join(desktop_path, "color", "teeth")              # 牙齒資料夾
dentalcrown_path = os.path.join(desktop_path, "color", "dentalcrown")  # 牙冠資料夾
dentin_path = os.path.join(desktop_path, "color", "Dentin")            # 象牙質資料夾
bw1_path = os.path.join(desktop_path, "bw", "gum_bw")                  # 黑白牙齦資料夾
bw2_path = os.path.join(desktop_path,"bw","teeth_bw")                  # 黑白牙齒資料夾
bw3_path = os.path.join(desktop_path, "bw","dentalcrown_bw")           # 黑白牙冠資料夾
bw4_path = os.path.join(desktop_path, "bw","dentin_bw")                # 黑白象牙質資料夾

# 確認資料夾存在，不存在則建立資料夾
os.makedirs(color_path, exist_ok=True)
os.makedirs(bw_path, exist_ok=True)
os.makedirs(desktop_path, exist_ok=True)
os.makedirs(desktop_path, exist_ok=True)
os.makedirs(gum_path, exist_ok=True)
os.makedirs(teeth_path, exist_ok=True)
os.makedirs(dentalcrown_path, exist_ok=True)
os.makedirs(dentin_path, exist_ok=True)
os.makedirs(bw1_path, exist_ok=True)
os.makedirs(bw2_path, exist_ok=True)
os.makedirs(bw3_path, exist_ok=True)
os.makedirs(bw4_path, exist_ok=True)

def retain_color(image, lower_bound, upper_bound, exclude_ranges=[]):
    # 將圖片從 BGR 轉換到 HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 創建遮罩，範圍內的顏色會變成白色，其餘的變成黑色
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # 排除指定範圍的顏色
    for exclude_lower, exclude_upper in exclude_ranges:
        exclude_mask = cv2.inRange(hsv, exclude_lower, exclude_upper)
        mask = cv2.bitwise_and(mask, cv2.bitwise_not(exclude_mask))
    
    # 膨脹和侵蝕處理
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) 
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.erode(mask, kernel, iterations=1)
    
    # 創建一個黑色圖像
    result = np.zeros_like(image)
    
    # 將原圖中的指定區域複製到結果圖像
    result[mask != 0] = image[mask != 0]
    
    # 高斯模糊後處理
    result = cv2.GaussianBlur(result, (5, 5), 0)
    return result

def remove_small_regions(binary_image, min_size):
    # 找出連通區域
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8)
    
    # 創建一個新的二值圖像，保留較大的區域
    new_image = np.zeros_like(binary_image)
    for i in range(1, num_labels):  # 跳過背景
        if stats[i, cv2.CC_STAT_AREA] >= min_size:
            new_image[labels == i] = 255
    
    return new_image

# 定義牙齦的 HSV 範圍
gum_lower = np.array([20, 78, 100])
gum_upper = np.array([35, 255, 255])

# 定義牙齒的 HSV 範圍
teeth_lower = np.array([100, 25, 52])
teeth_upper = np.array([170, 255, 255])

# 定義要排除的牙冠顏色範圍
exclude_ranges = [
    (np.array([0, 0, 0]), np.array([151, 35, 89])),       # 原定範圍1
    (np.array([156, 36, 32]), np.array([169, 117, 224])), # 原定範圍2
    (np.array([166, 84, 137]), np.array([166, 84, 137])), # 指定排除範圍1
    (np.array([157, 52, 44]), np.array([157, 52, 44])),   # 指定排除範圍2
    (np.array([165, 79, 90]), np.array([165, 79, 90])),   # 指定排除範圍3
    (np.array([167, 35, 225]), np.array([168, 39, 244]))  # 指定排除範圍4
]

# 定義牙冠的 HSV 範圍
dentalcrown_lower = np.array([152, 36, 90])
dentalcrown_upper = np.array([170, 150, 255])

# 定義象牙質的 HSV 範圍
dentin_lower = np.array([99, 47, 50])
dentin_upper = np.array([118, 180, 222])

# 處理並保存圖片(Color)
for filename in os.listdir(desktop_path):
    file_path = os.path.join(desktop_path, filename)
    if filename.endswith(".png"):
        # 讀取 PNG 圖片
        image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        if "color" in filename:
            bwfilename = filename.replace("color_", "")  # 移除 "color_"
        else:
            bwfilename = filename  # 如果不包含 "color"，保持原始檔名
        
        # 處理牙齦區域
        gum_result = retain_color(image, gum_lower, gum_upper)
        gum_output_path = os.path.join(gum_path, f"gum_{filename}")
        cv2.imwrite(gum_output_path, gum_result)
        
        # 轉換牙齦區域成 mask
        gum_gray = cv2.cvtColor(gum_result, cv2.COLOR_BGR2GRAY)
        _, gum_bw = cv2.threshold(gum_gray, 1, 255, cv2.THRESH_BINARY)
        gum_bw_output_path = os.path.join(bw1_path, f"gum_{bwfilename}")
        cv2.imwrite(gum_bw_output_path, gum_bw)
        
        # 處理牙齒區域
        teeth_result = retain_color(image, teeth_lower, teeth_upper)
        teeth_output_path = os.path.join(teeth_path, f"teeth_{filename}")
        cv2.imwrite(teeth_output_path, teeth_result)
        
        # 轉換牙齒區域成 mask
        teeth_gray = cv2.cvtColor(teeth_result, cv2.COLOR_BGR2GRAY)
        _, teeth_bw = cv2.threshold(teeth_gray, 1, 255, cv2.THRESH_BINARY)
        teeth_bw_output_path = os.path.join(bw2_path, f"teeth_{bwfilename}")
        cv2.imwrite(teeth_bw_output_path, teeth_bw)

        # 處理牙冠區域，並排除指定顏色範圍
        dentalcrown_result = retain_color(image, dentalcrown_lower, dentalcrown_upper, exclude_ranges)
        dentalcrown_output_path = os.path.join(dentalcrown_path, f"dentalcrown_{filename}")
        cv2.imwrite(dentalcrown_output_path, dentalcrown_result)
        
        # 轉換牙冠區域成 mask
        dentalcrown_gray = cv2.cvtColor(dentalcrown_result, cv2.COLOR_BGR2GRAY)
        _, dentalcrown_bw = cv2.threshold(dentalcrown_gray, 1, 255, cv2.THRESH_BINARY)
        # 移除小區域
        dentalcrown_bw = remove_small_regions(dentalcrown_bw, 1000)
        dentalcrown_bw_output_path = os.path.join(bw3_path, f"dentalcrown_{bwfilename}")
        cv2.imwrite(dentalcrown_bw_output_path, dentalcrown_bw)
        
        # 處理象牙質區域
        dentin_result = retain_color(image, dentin_lower, dentin_upper)
        dentin_output_path = os.path.join(dentin_path, f"dentin_{filename}")
        cv2.imwrite(dentin_output_path, dentin_result)
        
        # 轉換象牙質區域成 mask
        dentin_gray = cv2.cvtColor(dentin_result, cv2.COLOR_BGR2GRAY)
        _, dentin_bw = cv2.threshold(dentin_gray, 1, 255, cv2.THRESH_BINARY)
        # 移除小區域
        dentin_bw = remove_small_regions(dentin_bw, 1000)
        dentin_bw_output_path = os.path.join(bw4_path, f"dentin_{bwfilename}")
        cv2.imwrite(dentin_bw_output_path, dentin_bw)
        
        print(f"Results saved to {filename}")
print("All Works Done!")

