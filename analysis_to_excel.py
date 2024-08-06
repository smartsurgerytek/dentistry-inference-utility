import os
import pandas as pd
import re
from tkinter import Tk, Canvas, simpledialog, messagebox, Text, Scrollbar, VERTICAL, RIGHT, Y, BOTH, END
from PIL import Image, ImageTk, ImageDraw
import natsort

class ImageCropper:
    def __init__(self, root, image_path):
        self.root = root
        self.image_path = image_path
        self.image_files = self.get_image_files(os.path.dirname(image_path))
        self.current_image_index = self.image_files.index(image_path)
        
        self.canvas = Canvas(self.root)
        self.canvas.pack(side="left")
        
        self.scrollbar = Scrollbar(self.root, orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        self.text_box = Text(self.root, width=50, yscrollcommand=self.scrollbar.set)
        self.text_box.pack(side=RIGHT, fill=BOTH)
        self.scrollbar.config(command=self.text_box.yview)
        
        self.load_image()
        self.root.bind("<Control-s>", self.save_image)     # 保存圖片
        self.root.bind("<Control-z>", self.undo_last_point) # 撤銷最後一個點
        self.root.bind("<Control-n>", self.load_next_image) # 加載下一張圖片
        self.root.bind("<Control-b>", self.load_previous_image) # 加載上一張圖片  
        self.coords = []

    def get_image_files(self, directory):
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
        image_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(supported_formats)]
        return natsort.natsorted(image_files)  # 使用自然排序

    def load_image(self):
        self.image = Image.open(self.image_files[self.current_image_index])
        max_width = 640
        max_height = 480
        if self.image.width > max_width or self.image.height > max_height:
            self.image.thumbnail((max_width, max_height), Image.LANCZOS)
        
        self.photo = ImageTk.PhotoImage(self.image)
        
        canvas_width = self.image.width
        canvas_height = self.image.height
        
        self.canvas.config(width=canvas_width, height=canvas_height)
        self.canvas.delete("all")
        
        self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        
        self.canvas.bind("<Button-1>", self.get_click_coordinates)
        
        # 更新窗口標題為當前圖片名稱
        self.root.title(f"Image: {os.path.basename(self.image_files[self.current_image_index])}")

    def get_click_coordinates(self, event):
        # 顯示點擊的座標並在畫布上標註紅點
        x, y = event.x, event.y
        self.coords.append((x, y))
        
        img_width, img_height = self.image.size
        scaled_x = round(x * (1280 / img_width))
        scaled_y = round(y * (960 / img_height))
        
        self.text_box.insert(END, f'Click Point: ({scaled_x}, {scaled_y})\n')
        
        radius = 3
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='red')

    def save_image(self, event=None):
        draw_image = self.image.copy()
        draw = ImageDraw.Draw(draw_image)
        original_width, original_height = draw_image.size
        scaled_coords = []
        for (x, y) in self.coords:
            scaled_x = round(x * (original_width / self.image.width))
            scaled_y = round(y * (original_height / self.image.height))
            draw.ellipse((scaled_x - 3, scaled_y - 3, scaled_x + 3, scaled_y + 3), fill='red', outline='red')
            scaled_coords.append((scaled_x, scaled_y))
        
        image_filename = os.path.basename(self.image_files[self.current_image_index])
        image_number = re.findall(r'\d+', image_filename)
        if image_number:
            image_number = image_number[0]
        else:
            image_number = "0"
        
        save_path = os.path.join(os.path.dirname(self.image_files[self.current_image_index]),"redmark", f"redmark_{image_number}.png") # 標記後圖片儲存路徑
        excel_path = os.path.join(os.path.dirname(self.image_files[self.current_image_index]),"analysis",  f"analysis_{image_number}.xlsx") # Excel儲存路徑
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        os.makedirs(os.path.dirname(excel_path), exist_ok=True)
        # 檢查是否存在相同名稱的檔案
        if os.path.exists(save_path) or os.path.exists(excel_path):
            answer = messagebox.askyesno("File Already Exists", f'File {save_path}\n or {excel_path} already exists. Overwrite?')
            if not answer:    
                return
                # 如果不重覆儲存則結束程式
        
        draw_image = draw_image.resize((1280, 960), Image.LANCZOS) # 調整保存的圖片大小
        draw_image.save(save_path)
        
        # Excel的欄位名稱
        columns = [
            '牙齒ID（相對該張影像的順序ID即可、從左至右）',
            '牙尖ID（從左側至右側，看是連線到哪一個牙尖端）',
            '珐瑯質跟象牙質交接點x',
            '珐瑯質跟象牙質交接點y',
            '牙齦交接點x',
            '牙齦交接點y',
            '牙本體尖端點x',
            '牙本體尖端點y',
            '長度',
            'stage'
        ]
        
        df = pd.DataFrame(columns=columns)

        rows = []
        for i in range(0, len(scaled_coords), 3):
            # 跟 Columns 對應
            row = [None] * len(columns)
            if i < len(scaled_coords):
                row[2] = 2*scaled_coords[i][0]
                row[3] = 2*scaled_coords[i][1]
            if i + 1 < len(scaled_coords):
                row[4] = 2*scaled_coords[i + 1][0]
                row[5] = 2*scaled_coords[i + 1][1]
            if i + 2 < len(scaled_coords):
                row[6] = 2*scaled_coords[i + 2][0]
                row[7] = 2*scaled_coords[i + 2][1]
            rows.append(row)
        
        df = pd.concat([df, pd.DataFrame(rows, columns=columns)], ignore_index=True)
        
        with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, header=True)
            
            worksheet = writer.sheets['Sheet1']
            for i, col in enumerate(df.columns):
                max_len = max(df[col].astype(str).map(len).max(), len(col)) + 13 # 設定最大長度
                worksheet.set_column(i, i, max_len)
            
            workbook = writer.book
            cell_format = workbook.add_format({'bold': False})
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, cell_format)
        
        messagebox.showinfo("Success Saved Image", f'Image saved as: \n{save_path}\nCoordinates saved as: \n{excel_path}')
        print(f'Image saved as: {save_path}')       # 顯示圖片和座標檔案已儲存的提示
        print(f'Coordinates saved as: {excel_path}') # 並在控制台輸出儲存的檔案路徑
        
    def undo_last_point(self, event=None):
        # 撤銷最後一個點並重新顯示圖片及標註
        if self.coords:
            self.coords.pop()
            self.text_box.delete("end-2l", "end-1l")
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
            radius = 3
            for x, y in self.coords:
                self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='red')   
                # 重新繪製所有剩餘的點    

    def load_next_image(self, event=None):
        # 加載下一張圖片並顯示提示
        next_image_index = self.current_image_index + 1
        if next_image_index >= len(self.image_files):
            messagebox.showinfo("No More Images", "No more images to load")
            return
        self.coords = []
        self.text_box.delete(1.0, END)
        self.current_image_index = next_image_index
        self.image_path = self.image_files[self.current_image_index]
        self.load_image()
        messagebox.showinfo("Next Image", f'Load image: {self.image_files[self.current_image_index]}')
        # 顯示下一張圖片的提示

    def load_previous_image(self, event=None):
        # 加載上一張圖片並顯示提示
        previous_image_index = self.current_image_index - 1
        if previous_image_index < 0:
            messagebox.showinfo("No More Images", "No more previous images to load")
            return
        self.coords = []
        self.text_box.delete(1.0, END)
        self.current_image_index = previous_image_index
        self.image_path = self.image_files[self.current_image_index]
        self.load_image()
        messagebox.showinfo("Previous Image", f'Load image: {self.image_files[self.current_image_index]}')
        # 顯示上一張圖片的提示
        
    def show_help(self):
        help_message = (
            "Instructions:\n"
            "1. Click on the image to mark coordinate. Points will be shown as red dots.\n"
            "2. Use 'Ctrl + S' to save the current image with red marks.\n"
            "3. Use 'Ctrl + Z' to undo the last marked point.\n"
            "4. Use 'Ctrl + N' to load the next image in the directory.\n"
            "5. Use 'Ctrl + B' to load the previous image in the directory.\n"
            "6. Ensure the image path is correct when entering it initially.\n\n"
            "使用說明：\n"
            "1. 點擊圖片以標記座標。標記的點將顯示為紅色圓點。\n"
            "2. 使用 'Ctrl + S' 保存當前帶有紅色標記的圖片。\n"
            "3. 使用 'Ctrl + Z' 撤銷最後一個標記的點。\n"
            "4. 使用 'Ctrl + N' 加載目錄中的下一張圖片。\n"
            "5. 使用 'Ctrl + B' 加載目錄中的上一張圖片。\n"
            "6. 請確保初始輸入的圖片路徑是正確的。"
        )
        messagebox.showinfo("Help", help_message)

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    image_path = simpledialog.askstring("Locate Image Coordinates", "Enter your image path:")
    # 顯示輸入圖片路徑的對話框
    if image_path:
        image_path = image_path.strip('"').replace('/', '\\\\')
        # 去除雙引號並將斜線替換為斜線反斜線
        if os.path.isfile(image_path):
            root.deiconify()
            app = ImageCropper(root, image_path)
            app.show_help()  # 在確認圖片路徑後顯示幫助視窗
            root.mainloop()
        else:
            messagebox.showerror("Error", "Image file not found")
        # 提示用戶輸入圖片路徑
        # 如果文件存在則進入主程序，否則顯示錯誤信息
    else:
        messagebox.showinfo("Cancelled", "No image path provided")
        # 如果未提供圖片路徑，顯示取消提示
