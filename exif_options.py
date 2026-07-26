import customtkinter as ctk
import config, utils
import platform
from tkinter import PhotoImage

utils.resource_path("assets/logo.ico")


def open_exif_options(parent, exif_remove, toggle_callback):
    exif_window = ctk.CTkToplevel(parent)
    exif_window.title("EXIF Options")
    exif_window.geometry("400x600")

    if platform.system() == "Windows":
        exif_window.after(200, lambda: exif_window.iconbitmap(utils.resource_path("assets/logo.ico")))
    else:
        icon_img = PhotoImage(file=utils.resource_path("assets/logo.png"))
        exif_window.icon_img = icon_img
        exif_window.iconphoto(True, icon_img)

    try:
        exif_window.attributes("-topmost", True)
    except Exception:
        pass

    frame = ctk.CTkScrollableFrame(exif_window)

    # Create checkboxes for each EXIF category
    for section, fields in config.EXIF_FIELDS.items():
        ctk.CTkLabel(frame, text=section, font=ctk.CTkFont(size=16, weight="bold")).pack(side="top", fill="x", padx=10, pady=(10, 0))
        for key, tag_id, label in fields:
            var = ctk.IntVar(value=1 if exif_remove[key] else 0)
            checkbox = ctk.CTkCheckBox(frame, text=f"Remove {label}", variable=var, command=lambda k=key: toggle_callback(k))
            checkbox.pack(side="top", fill="x", padx=10, pady=5)
    frame.pack(fill="both", expand=True)

    return exif_window

