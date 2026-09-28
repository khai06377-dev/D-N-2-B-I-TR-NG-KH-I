import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# ================= Khởi tạo cửa sổ =================
root = tk.Tk()
root.title("Bài Tập Thực Hành Chương 2 - OpenCV")
root.geometry("1280x700")

cv_img = None
current_image_path = None

# ================= Hiển thị ảnh =================
def display_images(img1, title1, img2=None, title2="", img3=None, title3=""):
    lbl_title1.config(text=title1)
    lbl_title2.config(text=title2)
    lbl_title3.config(text=title3)

    list_img = [img1, img2, img3]
    list_lbl = [lbl_img1, lbl_img2, lbl_img3]

    for img, lbl in zip(list_img, list_lbl):
        if img is not None:
            resized = cv2.resize(img, (380, 320))

            if len(resized.shape) == 2:
                im_pil = Image.fromarray(resized)
            else:
                rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(rgb)

            img_tk = ImageTk.PhotoImage(im_pil)
            lbl.config(image=img_tk)
            lbl.image = img_tk
        else:
            lbl.config(image="")
            lbl.image = None


# ================= Chọn ảnh =================
def select_image():
    global cv_img, current_image_path

    path = filedialog.askopenfilename(
        title="Chọn ảnh xử lý",
        initialdir=r"C:\Users\LHUser\Pictures",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp")]
    )

    if path:
        current_image_path = path
        cv_img = cv2.imread(path)

        if cv_img is not None:
            run_bai_1()
        else:
            messagebox.showerror("Lỗi", "Không thể đọc tệp ảnh này!")


# ================= Bài 1 =================
def run_bai_1():
    if cv_img is None:
        return messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước!")

    pil_img = Image.open(current_image_path)
    pil_np = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    display_images(
        cv_img, "Bài 1: Đọc bằng OpenCV",
        pil_np, "Bài 1: Đọc bằng Pillow"
    )


# ================= Bài 2 =================
def run_bai_2():
    if cv_img is None:
        return messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước!")

    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)

    display_images(
        cv_img, "Ảnh gốc",
        gray, "Grayscale",
        hsv, "HSV"
    )


# ================= Bài 3 =================
def run_bai_3():
    if cv_img is None:
        return messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh chính trước!")

    path2 = filedialog.askopenfilename(
        title="Chọn ảnh thứ 2 cho Bài 3",
        initialdir=r"C:\Users\LHUser\Pictures",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp")]
    )

    if path2:
        img2 = cv2.imread(path2)

        if img2 is None:
            return messagebox.showerror("Lỗi", "Không thể đọc ảnh thứ hai!")

        h, w = cv_img.shape[:2]
        img2 = cv2.resize(img2, (w, h))

        result = cv2.bitwise_and(cv_img, img2)

        display_images(
            cv_img, "Ảnh 1",
            img2, "Ảnh 2",
            result, "Bitwise AND"
        )


# ================= Bài 4 =================
def run_bai_4():
    if cv_img is None:
        return messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước!")

    save_dir = os.path.dirname(current_image_path)

    cv2.imwrite(os.path.join(save_dir, "output_bai4.png"), cv_img)
    cv2.imwrite(os.path.join(save_dir, "output_bai4.jpg"), cv_img)
    cv2.imwrite(os.path.join(save_dir, "output_bai4.bmp"), cv_img)

    messagebox.showinfo(
        "Bài 4",
        f"Đã lưu PNG, JPG và BMP tại:\n{save_dir}"
    )


# ================= Bài 5 =================
def run_bai_5():
    if cv_img is None:
        return messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước!")

    value = np.ones(cv_img.shape, dtype="uint8") * 60

    bright = cv2.add(cv_img, value)
    dark = cv2.subtract(cv_img, value)

    display_images(
        cv_img, "Ảnh gốc",
        bright, "Tăng sáng (+60)",
        dark, "Giảm sáng (-60)"
    )


# ================= Bài 6 =================
def run_bai_6():
    if cv_img is None:
        return messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước!")

    h, w = cv_img.shape[:2]

    rotated = cv2.rotate(cv_img, cv2.ROTATE_90_CLOCKWISE)

    M = np.float32([[1, 0, 50],
                    [0, 1, 0]])
    shifted = cv2.warpAffine(cv_img, M, (w, h))

    scaled = cv2.resize(
        cv_img,
        None,
        fx=1.5,
        fy=1.5,
        interpolation=cv2.INTER_LINEAR
    )

    display_images(
        rotated, "Xoay 90°",
        shifted, "Dịch 50px",
        scaled, "Thu phóng 1.5x"
    )


# ================= Thanh công cụ =================
frame_toolbar = tk.Frame(root, padx=10, pady=10, bg="#f0f0f0")
frame_toolbar.pack(fill="x")

tk.Button(
    frame_toolbar,
    text="📁 Chọn ảnh từ máy tính",
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold"),
    command=select_image
).pack(side="left", padx=5)

buttons = [
    ("Bài 1", run_bai_1),
    ("Bài 2", run_bai_2),
    ("Bài 3", run_bai_3),
    ("Bài 4", run_bai_4),
    ("Bài 5", run_bai_5),
    ("Bài 6", run_bai_6),
]

for text, cmd in buttons:
    tk.Button(frame_toolbar, text=text, command=cmd).pack(side="left", padx=3)


# ================= Khung hiển thị =================
frame_main = tk.Frame(root, padx=10, pady=10)
frame_main.pack(fill="both", expand=True)

cols = []
titles = []
imgs = []

for i in range(3):
    col = tk.Frame(frame_main, highlightbackground="#ccc", highlightthickness=1)
    col.pack(side="left", fill="both", expand=True, padx=5)

    title = tk.Label(col, text=f"Khung {i+1}", font=("Arial", 11, "bold"))
    title.pack(pady=10)

    img = tk.Label(col)
    img.pack(expand=True)

    cols.append(col)
    titles.append(title)
    imgs.append(img)

lbl_title1, lbl_title2, lbl_title3 = titles
lbl_img1, lbl_img2, lbl_img3 = imgs

root.mainloop()