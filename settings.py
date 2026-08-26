from tkinter import filedialog, PhotoImage
from CTkMessagebox import CTkMessagebox
import config
import customtkinter as ctk
import platform
import sys
import os

import utils, exif_options

# Default settings
appearance_mode = "light"
output_folder = ""
thumb_size = 100
preserve_exif = False
exif_remove = dict(config.DEFAULT_EXIF_REMOVE)  # Initialize exif_remove with default values
exif_window = None

utils.resource_path("assets/logo.ico")  # Preload the resource path to avoid issues with PyInstaller


def save_settings():
    config.save_config(appearance_mode, output_folder, thumb_size, preserve_exif, exif_remove)

# Function to change theme
def theme(mode):
    global appearance_mode
    if mode == "light":
        appearance_mode = "dark"
        ctk.set_appearance_mode(appearance_mode)
    else:
        appearance_mode = "light"
        ctk.set_appearance_mode(appearance_mode)
    save_settings()

def exif_metadata(exif_button):
    global preserve_exif
    preserve_exif = not preserve_exif

    if not preserve_exif:
        for key in exif_remove:
            exif_remove[key] = False
        if exif_window is not None and exif_window.winfo_exists():
            exif_window.destroy()

    save_settings()
    exif_button.configure(state="normal" if preserve_exif else "disabled")

def toggle_exif_category(category):
    exif_remove[category] = not exif_remove[category]
    save_settings()

# Function to update thumbnail size
def update_thumbnail_size(value, label):
    global thumb_size
    thumb_size = value
    label.configure(text=f"Thumbnail size: {int(value)}")

# Function to select output folder
def select_folder(label):
    global output_folder
    # Using /home for Linux because starting from / is not user-friendly
    initial_dir = "/" if platform.system() == "Windows" else "/home"
    chosen_folder = filedialog.askdirectory(initialdir=initial_dir, title="Select output folder")

    if chosen_folder:
        output_folder = chosen_folder
        label.configure(text=output_folder)
        CTkMessagebox(title="Done", message="Selected output folder: " + output_folder, icon="check")
        save_settings()

def show_exif_options(app):
    global exif_window
    if exif_window is None or not exif_window.winfo_exists():
        exif_window = exif_options.open_exif_options(app, exif_remove, toggle_exif_category)
    else:
        exif_window.lift()
        exif_window.focus_force()

def open_settings(app, check_updates_callback):
    settings_window = ctk.CTkToplevel(master=app)
    settings_window.title("Settings")
    settings_window.geometry("300x375")
    try:
        settings_window.attributes("-topmost", True)
    except Exception:
        pass

    if platform.system() == "Windows":
        settings_window.after(200, lambda: settings_window.iconbitmap(utils.resource_path("assets/logo.ico")))
    else:
        icon_img = PhotoImage(file=utils.resource_path("assets/logo.png"))
        settings_window.icon_img = icon_img
        settings_window.iconphoto(True, icon_img)

    switch_var = ctk.IntVar(value=1 if appearance_mode == "dark" else 0)
    switch_mode = ctk.CTkSwitch(settings_window, text="Dark mode", variable=switch_var, command=lambda: theme("light" if switch_var.get() == 1 else "dark"))

    switch_exif_var = ctk.IntVar(value=1 if preserve_exif else 0)
    switch_exif = ctk.CTkSwitch(settings_window, text="Preserve EXIF metadata", variable=switch_exif_var, command=lambda: exif_metadata(exif_button))

    exif_button = ctk.CTkButton(settings_window, text="More EXIF options", command=lambda: show_exif_options(settings_window))
    exif_button.configure(state="normal" if preserve_exif else "disabled")

    folder_label = ctk.CTkLabel(settings_window, text=output_folder if output_folder != "" else "No folder selected")
    folder_button = ctk.CTkButton(settings_window, text="Select output folder",command=lambda: select_folder(folder_label))

    thumbSize_label = ctk.CTkLabel(settings_window, text=f"Thumbnail size: {int(thumb_size)}")
    thumbSize_slider = ctk.CTkSlider(settings_window, from_=50, to=200, command=lambda v: update_thumbnail_size(v, thumbSize_label))
    thumbSize_slider.set(thumb_size)
    thumbSize_slider.bind("<ButtonRelease-1>", lambda e: save_settings())

    # What you can see
    switch_mode.pack(side="top", fill="x", padx=10, pady=5)
    switch_exif.pack(side="top", fill="x", padx=10)
    exif_button.pack(side="top", fill="x", padx=10, pady=5)

    update_button = ctk.CTkButton(settings_window, text="Check for updates", command=lambda: check_updates_callback(silent=False))
    update_button.pack(side="bottom", fill="x", padx=10, pady=5)

    folder_button.pack(side="bottom", fill="x", padx=10, pady=5)
    folder_label.pack(side="bottom", fill="x", padx=10, pady=1)

    thumbSize_slider.pack(side="bottom", fill="x", padx=10, pady=20)
    thumbSize_label.pack(side="bottom", fill="x", padx=10, pady=1)

    return settings_window
