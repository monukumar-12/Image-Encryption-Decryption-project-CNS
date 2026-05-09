# =========================================================
# ADVANCED DES IMAGE ENCRYPTION & DECRYPTION GUI
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
# GUI SETTINGS
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("DES Image Encryption & Decryption")
app.geometry("1000x700")
app.resizable(False, False)

selected_file = ""

# =========================================================
# GENERATE DES KEY
# =========================================================

def generate_key(password):
    return md5(password.encode()).digest()[:8]

# =========================================================
# IMAGE PREVIEW
# =========================================================

def show_image(path):
    img = Image.open(path)
    img = img.resize((350, 350))

    photo = ImageTk.PhotoImage(img)

    image_label.configure(image=photo, text="")
    image_label.image = photo

# =========================================================
# BROWSE IMAGE
# =========================================================

def browse_image():
    global selected_file

    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")
        ]
    )

    if file_path:
        selected_file = file_path
        file_name.configure(text=os.path.basename(file_path))
        show_image(file_path)

# =========================================================
# ENCRYPT IMAGE
# =========================================================

# =========================================================
# ENCRYPT IMAGE
# =========================================================

def encrypt_image():

    global selected_file

    if selected_file == "":
        messagebox.showerror("Error", "Please Select Image")
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

            # =========================================
            # CLEAR IMAGE PREVIEW AFTER ENCRYPTION
            # =========================================

            image_label.configure(
                image="",
                text="IMAGE ENCRYPTED\nPreview Hidden"
            )

            image_label.image = None

            # REMOVE FILE NAME
            file_name.configure(text="No Image Selected")

            # CLEAR PASSWORD
            password_entry.delete(0, 'end')

            # RESET SELECTED FILE
            selected_file = ""

            # STATUS
            status_label.configure(
                text=f"Image Encrypted Successfully in {round(end-start,2)} sec",
                text_color="lightgreen"
            )

            messagebox.showinfo(
                "Success",
                f"Encrypted File Saved Successfully\n\n{output_file}"
            )

    except Exception as e:
        messagebox.showerror("Error", str(e))

# =========================================================
# DECRYPT IMAGE
# =========================================================

def decrypt_image():

    encrypted_file = filedialog.askopenfilename(
        title="Select Encrypted File",
        filetypes=[("DES Files", "*.des")]
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

            status_label.configure(
                text=f"Image Decrypted Successfully in {round(end-start,2)} sec",
                text_color="cyan"
            )

            # CLEAR PASSWORD AFTER DECRYPTION
            password_entry.delete(0, 'end')

            messagebox.showinfo(
                "Success",
                f"Decrypted Image Saved:\n{output_file}"
            )

    except Exception:
        messagebox.showerror(
            "Error",
            "Wrong Password or Corrupted File"
        )

# =========================================================
# TITLE
# =========================================================

title = ctk.CTkLabel(
    app,
    text="ADVANCED DES IMAGE SECURITY SYSTEM",
    font=("Arial", 30, "bold")
)

title.pack(pady=20)

# =========================================================
# MAIN FRAME
# =========================================================

main_frame = ctk.CTkFrame(app, width=900, height=500)
main_frame.pack(pady=10)

# =========================================================
# IMAGE PREVIEW
# =========================================================

image_label = ctk.CTkLabel(
    main_frame,
    text="IMAGE PREVIEW",
    width=350,
    height=350,
    corner_radius=15
)

image_label.place(x=40, y=50)

# =========================================================
# RIGHT SIDE PANEL
# =========================================================

side_frame = ctk.CTkFrame(main_frame, width=400, height=400)
side_frame.place(x=470, y=50)

# =========================================================
# FILE NAME
# =========================================================

file_name = ctk.CTkLabel(
    side_frame,
    text="No Image Selected",
    font=("Arial", 16)
)

file_name.pack(pady=20)

# =========================================================
# PASSWORD ENTRY
# =========================================================

password_entry = ctk.CTkEntry(
    side_frame,
    width=300,
    height=45,
    placeholder_text="Enter Secret Password",
    show="*",
    font=("Arial", 16)
)

password_entry.pack(pady=20)

# =========================================================
# BUTTONS
# =========================================================

browse_btn = ctk.CTkButton(
    side_frame,
    text="Browse Image",
    width=250,
    height=45,
    command=browse_image,
    font=("Arial", 16, "bold")
)

browse_btn.pack(pady=15)

encrypt_btn = ctk.CTkButton(
    side_frame,
    text="Encrypt Image",
    width=250,
    height=45,
    fg_color="green",
    hover_color="darkgreen",
    command=encrypt_image,
    font=("Arial", 16, "bold")
)

encrypt_btn.pack(pady=15)

decrypt_btn = ctk.CTkButton(
    side_frame,
    text="Decrypt Image",
    width=250,
    height=45,
    fg_color="red",
    hover_color="darkred",
    command=decrypt_image,
    font=("Arial", 16, "bold")
)

decrypt_btn.pack(pady=15)

# =========================================================
# STATUS LABEL
# =========================================================

status_label = ctk.CTkLabel(
    app,
    text="System Ready",
    font=("Arial", 16)
)

status_label.pack(pady=20)

# =========================================================
# FOOTER
# =========================================================

footer = ctk.CTkLabel(
    app,
    text="Cyber Security Project | DES Cryptography",
    font=("Arial", 14)
)

footer.pack(side="bottom", pady=15)

# =========================================================
# RUN APPLICATION
# =========================================================

app.mainloop()