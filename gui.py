import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os

from image_processing import (
    convert_to_grayscale,
    adjust_brightness,
    horizontal_flip,
    convert_to_black_white
)


class MatrixVisionGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("MatrixVision | Image Processing")
        self.root.geometry("1100x850")
        self.root.minsize(900, 750)
        self.root.configure(bg="#FFF5F8")

        # Image variables
        self.original_image = None
        self.processed_image = None
        self.original_photo = None
        self.processed_photo = None

        # Deep Pink Theme
        self.BACKGROUND = "#FFF5F8"
        self.WHITE = "#FFFFFF"
        self.PINK = "#C94F83"
        self.DARK_PINK = "#A83265"
        self.LIGHT_PINK = "#FCE4ED"
        self.TEXT = "#71364F"
        self.GRAY = "#98677D"

        self.create_interface()

    # =====================================
    # MAIN INTERFACE
    # =====================================

    def create_interface(self):

        # Header
        header = tk.Frame(
            self.root,
            bg=self.BACKGROUND
        )
        header.pack(fill="x", pady=(20, 5))

        tk.Label(
            header,
            text="MatrixVision",
            font=("Arial", 30, "bold"),
            bg=self.BACKGROUND,
            fg=self.DARK_PINK
        ).pack()

        tk.Label(
            header,
            text="IMAGE PROCESSING USING MATRICES",
            font=("Arial", 11, "bold"),
            bg=self.BACKGROUND,
            fg=self.GRAY
        ).pack(pady=5)

        tk.Label(
            header,
            text="Transform your images using mathematical matrices",
            font=("Arial", 10),
            bg=self.BACKGROUND,
            fg=self.TEXT
        ).pack(pady=3)

        # Open Image Button
        self.open_button = tk.Button(
            self.root,
            text="+  OPEN IMAGE",
            command=self.open_image,
            font=("Arial", 13, "bold"),
            bg=self.DARK_PINK,
            fg=self.WHITE,
            activebackground=self.PINK,
            activeforeground=self.WHITE,
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=12
        )
        self.open_button.pack(pady=15)

        # Image Information
        self.info_label = tk.Label(
            self.root,
            text="Choose an image from your computer",
            font=("Arial", 10),
            bg=self.BACKGROUND,
            fg=self.GRAY
        )
        self.info_label.pack(pady=5)

        # Images Section
        images_frame = tk.Frame(
            self.root,
            bg=self.BACKGROUND
        )
        images_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        images_frame.columnconfigure(0, weight=1)
        images_frame.columnconfigure(1, weight=1)

        # Original Image Card
        original_card = tk.LabelFrame(
            images_frame,
            text="ORIGINAL IMAGE",
            font=("Arial", 12, "bold"),
            bg=self.WHITE,
            fg=self.DARK_PINK,
            bd=2,
            relief="groove"
        )
        original_card.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        self.original_view = tk.Label(
            original_card,
            text="No Image Selected",
            font=("Arial", 11),
            bg=self.LIGHT_PINK,
            fg=self.GRAY,
            width=40,
            height=15
        )
        self.original_view.pack(
            padx=12,
            pady=12,
            fill="both",
            expand=True
        )

        # Processed Image Card
        processed_card = tk.LabelFrame(
            images_frame,
            text="PROCESSED IMAGE",
            font=("Arial", 12, "bold"),
            bg=self.WHITE,
            fg=self.DARK_PINK,
            bd=2,
            relief="groove"
        )
        processed_card.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        self.processed_view = tk.Label(
            processed_card,
            text="Processed Image Will Appear Here",
            font=("Arial", 11),
            bg=self.LIGHT_PINK,
            fg=self.GRAY,
            width=40,
            height=15
        )
        self.processed_view.pack(
            padx=12,
            pady=12,
            fill="both",
            expand=True
        )

        # Processing Tools Title
        tk.Label(
            self.root,
            text="IMAGE PROCESSING TOOLS",
            font=("Arial", 13, "bold"),
            bg=self.BACKGROUND,
            fg=self.DARK_PINK
        ).pack(pady=(10, 5))

        # Buttons
        buttons_frame = tk.Frame(
            self.root,
            bg=self.BACKGROUND
        )
        buttons_frame.pack(pady=5)

        self.buttons = []

        self.add_button(
            buttons_frame,
            "Grayscale",
            self.grayscale,
            0, 0
        )

        self.add_button(
            buttons_frame,
            "Horizontal Flip",
            self.flip,
            0, 1
        )

        self.add_button(
            buttons_frame,
            "Black & White",
            self.black_white,
            0, 2
        )

        self.add_button(
            buttons_frame,
            "Reset",
            self.reset,
            1, 0
        )

        self.add_button(
            buttons_frame,
            "Save Image",
            self.save_image,
            1, 1
        )

        self.add_button(
            buttons_frame,
            "Clear Image",
            self.clear_image,
            1, 2
        )

        # Brightness Section
        brightness_frame = tk.Frame(
            self.root,
            bg=self.BACKGROUND
        )
        brightness_frame.pack(pady=10)

        tk.Label(
            brightness_frame,
            text="BRIGHTNESS ADJUSTMENT",
            font=("Arial", 12, "bold"),
            bg=self.BACKGROUND,
            fg=self.DARK_PINK
        ).pack()

        self.brightness_slider = tk.Scale(
            brightness_frame,
            from_=-100,
            to=100,
            orient="horizontal",
            length=400,
            resolution=1,
            bg=self.BACKGROUND,
            fg=self.TEXT,
            troughcolor="#D98AAA",
            activebackground=self.DARK_PINK,
            highlightthickness=0,
            command=self.brightness
        )
        self.brightness_slider.pack()

        # Footer
        tk.Label(
            self.root,
            text="MatrixVision | Python | NumPy | Tkinter",
            font=("Arial", 9),
            bg=self.BACKGROUND,
            fg=self.GRAY
        ).pack(pady=12)

        self.set_buttons_state("disabled")

    # =====================================
    # CREATE BUTTONS
    # =====================================

    def add_button(self, parent, text, command, row, col):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            width=18,
            height=2,
            font=("Arial", 10, "bold"),
            bg=self.PINK,
            fg=self.WHITE,
            activebackground=self.DARK_PINK,
            activeforeground=self.WHITE,
            disabledforeground="#C9A6B5",
            relief="flat",
            cursor="hand2"
        )

        button.grid(
            row=row,
            column=col,
            padx=8,
            pady=7
        )

        self.buttons.append(button)

    # =====================================
    # BUTTON STATES
    # =====================================

    def set_buttons_state(self, state):

        for button in self.buttons:
            button.config(state=state)

        self.brightness_slider.config(state=state)

    # =====================================
    # OPEN IMAGE
    # =====================================

    def open_image(self):

        path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image Files",
                 "*.jpg *.jpeg *.png *.bmp *.tiff")
            ]
        )

        if not path:
            return

        try:

            image = Image.open(path).convert("RGB")

            self.original_image = np.array(image)
            self.processed_image = self.original_image.copy()

            height, width, channels = self.original_image.shape

            filename = os.path.basename(path)

            self.info_label.config(
                text=f"{filename} | Width: {width} | "
                     f"Height: {height} | RGB"
            )

            self.show_image(
                self.original_image,
                self.original_view,
                "original"
            )

            self.show_image(
                self.processed_image,
                self.processed_view,
                "processed"
            )

            self.set_buttons_state("normal")
            self.brightness_slider.set(0)

        except Exception as error:

            messagebox.showerror(
                "Image Error",
                str(error)
            )

    # =====================================
    # DISPLAY IMAGE
    # =====================================

    def show_image(self, image_array, label, image_type):

        image = Image.fromarray(image_array)
        image.thumbnail((420, 300))

        photo = ImageTk.PhotoImage(image)

        label.config(
            image=photo,
            text="",
            bg=self.WHITE
        )

        if image_type == "original":
            self.original_photo = photo
        else:
            self.processed_photo = photo

    # =====================================
    # CHECK IMAGE
    # =====================================

    def check_image(self):

        if self.original_image is None:

            messagebox.showwarning(
                "Warning",
                "Please open an image first!"
            )

            return False

        return True

    # =====================================
    # GRAYSCALE
    # =====================================

    def grayscale(self):

        if not self.check_image():
            return

        self.brightness_slider.set(0)

        self.processed_image = convert_to_grayscale(
            self.original_image
        )

        self.show_image(
            self.processed_image,
            self.processed_view,
            "processed"
        )

    # =====================================
    # BRIGHTNESS
    # =====================================

    def brightness(self, value):

        if self.original_image is None:
            return

        value = int(float(value))

        self.processed_image = adjust_brightness(
            self.original_image,
            value
        )

        self.show_image(
            self.processed_image,
            self.processed_view,
            "processed"
        )

    # =====================================
    # HORIZONTAL FLIP
    # =====================================

    def flip(self):

        if not self.check_image():
            return

        self.brightness_slider.set(0)

        self.processed_image = horizontal_flip(
            self.original_image
        )

        self.show_image(
            self.processed_image,
            self.processed_view,
            "processed"
        )

    # =====================================
    # BLACK AND WHITE
    # =====================================

    def black_white(self):

        if not self.check_image():
            return

        self.brightness_slider.set(0)

        self.processed_image = convert_to_black_white(
            self.original_image
        )

        self.show_image(
            self.processed_image,
            self.processed_view,
            "processed"
        )

    # =====================================
    # RESET
    # =====================================

    def reset(self):

        if not self.check_image():
            return

        self.brightness_slider.set(0)

        self.processed_image = self.original_image.copy()

        self.show_image(
            self.processed_image,
            self.processed_view,
            "processed"
        )

    # =====================================
    # SAVE IMAGE
    # =====================================

    def save_image(self):

        if not self.check_image():
            return

        path = filedialog.asksaveasfilename(
            title="Save Processed Image",
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("BMP Image", "*.bmp")
            ]
        )

        if not path:
            return

        try:

            Image.fromarray(
                self.processed_image
            ).save(path)

            messagebox.showinfo(
                "Success",
                "Image saved successfully!"
            )

        except Exception as error:

            messagebox.showerror(
                "Save Error",
                str(error)
            )

    # =====================================
    # CLEAR IMAGE
    # =====================================

    def clear_image(self):

        self.original_image = None
        self.processed_image = None

        self.original_photo = None
        self.processed_photo = None

        self.original_view.config(
            image="",
            text="No Image Selected",
            bg=self.LIGHT_PINK,
            fg=self.GRAY
        )

        self.processed_view.config(
            image="",
            text="Processed Image Will Appear Here",
            bg=self.LIGHT_PINK,
            fg=self.GRAY
        )

        self.info_label.config(
            text="Choose an image from your computer"
        )

        self.brightness_slider.set(0)

        self.set_buttons_state("disabled")