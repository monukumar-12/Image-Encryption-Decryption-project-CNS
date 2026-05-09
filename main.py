# =========================================================
# PROFESSIONAL DES IMAGE ENCRYPTION & DECRYPTION SYSTEM
# =========================================================

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from hashlib import md5
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
import os
import time

# =========================================================
# INSTALL:
# pip install pycryptodome pillow customtkinter
# =========================================================

# =========================================================
# APP SETTINGS
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("1200x750")
app.title("Enterprise DES Image Security Suite")
app.resizable(False, False)

selected_file = ""

# =========================================================
# KEY GENERATION
# =========================================================

def generate_key(password):
    return md5(password.encode()).digest()[:8]

# =========================================================
# SHOW IMAGE
# =========================================================

def show_image(path):

    img = Image.open(path)
    img = img.resize((420, 420))

    photo = ImageTk.PhotoImage(img)

    preview_label.configure(image=photo, text="")
    preview_label.image = photo

# =========================================================
# SELECT IMAGE
# =========================================================

def browse_image():

    global selected_file

    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )

    if file_path:

        selected_file = file_path
        image_name.configure(text=os.path.basename(file_path))
        show_image(file_path)

# =========================================================
# ENCRYPT IMAGE
# =========================================================

def encrypt_image():

    global selected_file

    if selected_file == "":
        messagebox.showerror("Error", "Select Image First")
        return

    password = password_entry.get()

    if password == "":
        messagebox.showerror("Error", "Enter Password")
        return

    try:

        start = time.time()

        key = generate_key(password)

        cipher = DES.new(key, DES.MODE_CBC)

        with open(selected_file, 'rb') as f:
            data = f.read()

        padded_data = pad(data, DES.block_size)

        encrypted_data = cipher.encrypt(padded_data)

        output_file = filedialog.asksaveasfilename(
            title="Save Encrypted File",
            defaultextension=".des",
            filetypes=[("DES File", "*.des")]
        )

        if output_file:

            with open(output_file, 'wb') as f:
                f.write(cipher.iv)
                f.write(encrypted_data)

            end = time.time()

            # REMOVE PREVIEW
            preview_label.configure(
                image="",
                text="IMAGE ENCRYPTED\nPreview Hidden"
            )

            preview_label.image = None

            # CLEAR PASSWORD
            password_entry.delete(0, 'end')

            # RESET IMAGE
            selected_file = ""
            image_name.configure(text="No Image Selected")

            status_label.configure(
                text=f"Encryption Completed in {round(end-start,2)} sec",
                text_color="#00ff99"
            )

            messagebox.showinfo(
                "Success",
                "Image Encrypted Successfully"
            )

    except Exception as e:
        messagebox.showerror("Error", str(e))

# =========================================================
# DECRYPT IMAGE
# =========================================================

def decrypt_image():

    encrypted_file = filedialog.askopenfilename(
        title="Select Encrypted File",
        filetypes=[("DES File", "*.des")]
    )

    if encrypted_file == "":
        return

    password = password_entry.get()

    if password == "":
        messagebox.showerror("Error", "Enter Password")
        return

    try:

        start = time.time()

        key = generate_key(password)

        with open(encrypted_file, 'rb') as f:
            iv = f.read(8)
            encrypted_data = f.read()

        cipher = DES.new(key, DES.MODE_CBC, iv=iv)

        decrypted_data = unpad(
            cipher.decrypt(encrypted_data),
            DES.block_size
        )

        output_file = filedialog.asksaveasfilename(
            title="Save Decrypted Image",
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPG", "*.jpg"),
                ("JPEG", "*.jpeg")
            ]
        )

        if output_file:

            with open(output_file, 'wb') as f:
                f.write(decrypted_data)

            end = time.time()

            show_image(output_file)

            password_entry.delete(0, 'end')

            status_label.configure(
                text=f"Decryption Completed in {round(end-start,2)} sec",
                text_color="#00ccff"
            )

            messagebox.showinfo(
                "Success",
                "Image Decrypted Successfully"
            )

    except Exception:
        messagebox.showerror(
            "Error",
            "Wrong Password or Corrupted File"
        )

# =========================================================
# HEADER
# =========================================================

header = ctk.CTkFrame(app, height=80, corner_radius=0)
header.pack(fill="x")

heading = ctk.CTkLabel(
    header,
    text="ENTERPRISE DES IMAGE SECURITY SUITE",
    font=("Montserrat", 32, "bold"),
    text_color="#00d4ff"
)

heading.pack(pady=20)

# =========================================================
# MAIN AREA
# =========================================================

main_frame = ctk.CTkFrame(
    app,
    width=1150,
    height=580,
    corner_radius=25
)

main_frame.pack(pady=25)

# =========================================================
# LEFT PANEL
# =========================================================

left_panel = ctk.CTkFrame(
    main_frame,
    width=500,
    height=520,
    corner_radius=20
)

left_panel.place(x=30, y=30)

preview_title = ctk.CTkLabel(
    left_panel,
    text="IMAGE PREVIEW",
    font=("Arial", 24, "bold")
)

preview_title.pack(pady=15)

preview_label = ctk.CTkLabel(
    left_panel,
    text="No Image Selected",
    width=420,
    height=420,
    corner_radius=15,
    fg_color="#1a1a1a"
)

preview_label.pack(pady=10)

# =========================================================
# RIGHT PANEL
# =========================================================

right_panel = ctk.CTkFrame(
    main_frame,
    width=520,
    height=520,
    corner_radius=20
)

right_panel.place(x=590, y=30)

system_title = ctk.CTkLabel(
    right_panel,
    text="SECURITY CONTROL PANEL",
    font=("Arial", 26, "bold"),
    text_color="#00ffcc"
)

system_title.pack(pady=25)

image_name = ctk.CTkLabel(
    right_panel,
    text="No Image Selected",
    font=("Arial", 16)
)

image_name.pack(pady=10)

password_entry = ctk.CTkEntry(
    right_panel,
    width=350,
    height=50,
    placeholder_text="Enter Secure Password",
    show="*",
    font=("Arial", 18),
    corner_radius=12
)

password_entry.pack(pady=30)

browse_btn = ctk.CTkButton(
    right_panel,
    text="Browse Image",
    width=300,
    height=55,
    font=("Arial", 18, "bold"),
    corner_radius=15,
    command=browse_image
)

browse_btn.pack(pady=15)

encrypt_btn = ctk.CTkButton(
    right_panel,
    text="Encrypt Image",
    width=300,
    height=55,
    font=("Arial", 18, "bold"),
    fg_color="#00aa55",
    hover_color="#007733",
    corner_radius=15,
    command=encrypt_image
)

encrypt_btn.pack(pady=15)

decrypt_btn = ctk.CTkButton(
    right_panel,
    text="Decrypt Image",
    width=300,
    height=55,
    font=("Arial", 18, "bold"),
    fg_color="#cc3333",
    hover_color="#991111",
    corner_radius=15,
    command=decrypt_image
)

decrypt_btn.pack(pady=15)

status_label = ctk.CTkLabel(
    right_panel,
    text="System Ready",
    font=("Arial", 16, "bold")
)

status_label.pack(pady=25)

footer = ctk.CTkLabel(
    app,
    text="Cyber Security Project | DES Cryptography | Enterprise Edition",
    font=("Arial", 14)
)

footer.pack(side="bottom", pady=10)

# =========================================================
# RUN APPLICATION
# =========================================================

app.mainloop()