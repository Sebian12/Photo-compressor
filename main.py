import os
import customtkinter as ctk
from tkinter import filedialog, PhotoImage
from CTkMessagebox import CTkMessagebox
from PIL import Image
import sys
import platform

# File import
import settings, config, utils

# Important global variables
selected_files = []
settings_win = None
file_labels = {}
thumbnail_refs = {}
remove_buttons = {}

# Load settings
settings_saver = config.load_config()
settings.appearance_mode = settings_saver["appearance_mode"]
settings.output_folder = settings_saver["output_folder"]
settings.thumb_size = settings_saver.get("thumb_size", 100)
settings.preserve_exif = settings_saver.get("preserve_exif", False)
settings.exif_remove = settings_saver.get("exif_remove", dict(config.DEFAULT_EXIF_REMOVE))

# Megabyte constant
MB = 1024 * 1024

utils.resource_path("assets/logo.ico")  # Preload the resource path to avoid issues with PyInstaller

# Function to remove file from list
def remove_file(file, row):
    selected_files.remove(file)
    del thumbnail_refs[file]
    del file_labels[file]
    del remove_buttons[file]
    row.destroy()
    counter_lbl.configure(text=f"Selected files: {len(selected_files)}")
    before_space_lbl.configure(text="Before: -")
    after_space_lbl.configure(text="New size: -")
    progress.set(0)

# Function to select files
def select_photos():
    skipped = 0
    if platform.system() == "Windows":
        filetypes = (("Photos", "*.png *.jpg *.jpeg *.avif *.webp"), ("All Files", "*.*"))
        initial_dir = "/"
    else:
        # Known issues - while using Photos filter it doesn't see .jpg files
        filetypes = (("All Files", "*.*"), ("Photos", "*.png *.jpg *.jpeg *.avif *.webp"))
        # starting from /home in Linux because starting from / is not user-friendly
        initial_dir = "/home"

    filename = filedialog.askopenfilenames(initialdir=initial_dir, title="Select file", filetypes=filetypes)

    if filename:
        for file in filename:
            if file not in selected_files:
                row = ctk.CTkFrame(files_frame, fg_color="transparent")

                try:
                    thumbnails = Image.open(file)
                    # Resize thumbnail to the specified size in settings
                    thumbnails.thumbnail((settings.thumb_size, settings.thumb_size))
                    thumb_img = ctk.CTkImage(light_image=thumbnails, dark_image=thumbnails, size=(settings.thumb_size, settings.thumb_size))
                    thumb_lbl = ctk.CTkLabel(row, image=thumb_img, text="")
                    thumbnails.close()
                    thumb_lbl.pack(side="left", padx=10, pady=10)
                    thumbnail_refs[file] = thumb_img

                except (OSError, Image.UnidentifiedImageError):
                    CTkMessagebox(title="ERROR05", message="Cannot load thumbnail for: " + os.path.basename(file), icon="cancel")
                    row.destroy()
                    continue

                remove_btn = ctk.CTkButton(row, text="X", width=30, command=lambda f=file, r=row: remove_file(f, r))
                remove_btn.pack(side="right", pady=5)
                remove_buttons[file] = remove_btn
                lbl = ctk.CTkLabel(row, text=f"{os.path.basename(file)} — {os.path.getsize(file) / MB:.2f} MB")
                lbl.pack(side="left", padx=10)
                file_labels[file] = lbl
                row.pack(fill="x")
                selected_files.append(file)
            else:
                skipped += 1
            counter_lbl.configure(text=f"Selected files: {len(selected_files)}")
        if skipped > 0:
            CTkMessagebox(title="WARNING02", message=f"{skipped} file(s) already selected!", icon="warning")

def lock_ui():
    btn_compress.configure(state="disabled")
    settings_button.configure(state="disabled")
    clear_list_btn.configure(state="disabled")

    drop_frame.unbind("<Button-1>")
    drop_label.unbind("<Button-1>")
    for btn in remove_buttons.values():
        btn.configure(state="disabled")
    
def unlock_ui():
    btn_compress.configure(state="normal")
    clear_list_btn.configure(state="normal")
    settings_button.configure(state="normal")

    drop_frame.bind("<Button-1>", lambda e: select_photos())
    drop_label.bind("<Button-1>", lambda e: select_photos())
    for btn in remove_buttons.values():
        btn.configure(state="normal")

# Function that compresses a single file and returns its before/after size,
# or None if the file was skipped (unsupported, missing, corrupted, or save error)
def compress_single_file(file, compress_value, used_paths):
    name, ext = os.path.splitext(file)

    # Checks file type
    if ext.lower() not in [".jpg", ".jpeg", ".png", ".webp", ".avif"]:
        CTkMessagebox(title="ERROR02", message="File not supported!", icon="cancel")
        return None

    # Checks if file exists
    if not os.path.exists(file):
        # If not throws an error
        CTkMessagebox(title="ERROR03", message="File  " + os.path.basename(file) + "  doesn't exist!", icon="cancel")
        return None
    file_size = os.path.getsize(file)
    try:
        img = Image.open(file)
    except (OSError, Image.UnidentifiedImageError):
        CTkMessagebox(title="ERROR04", message="File corrupted or doesn't exist!", icon="cancel")
        return None
        # Only touch EXIF at all if the user actually wants it kept
    if settings.preserve_exif:
        try:
            exif_data = img.getexif()
            exif_sub_ifd = exif_data.get_ifd(0x8769)
            for fields in config.EXIF_FIELDS.values():
                for key, tag_id, _ in fields:
                    if settings.exif_remove[key]:
                        exif_data.pop(tag_id, None)
                        exif_sub_ifd.pop(tag_id, None)
        except (OSError, Image.UnidentifiedImageError):
            img.close()
            CTkMessagebox(title="ERROR10", message="Couldn't load exif metadata. File skipped.", icon="cancel")
            return None
    else:
        exif_data = None

    # Checking if user selected output folder
    if settings.output_folder != "":
        base_path = os.path.join(settings.output_folder, os.path.basename(name) + "_compressed" + ext)
    else:
        base_path = name + "_compressed" + ext

    # Avoid two different source files (e.g. same filename from two
    # different folders) silently overwriting each other's output
    # within the same batch
    output_path = base_path
    counter = 1
    while output_path in used_paths or os.path.exists(output_path):
        output_path = os.path.splitext(base_path)[0] + f"_{counter}" + ext
        counter += 1
    was_renamed = output_path != base_path
    used_paths.add(output_path)

    try:
        # Compression is different in .jpg and .png
        if ext.lower() in [".jpg", ".jpeg", ".webp", ".avif"]:
            if exif_data is not None:
                img.save(output_path, quality=compress_value, exif=exif_data)
            else:
                img.save(output_path, quality=compress_value)
        elif ext.lower() == ".png":
            if exif_data is not None:
                img.save(output_path, compress_level=(100 - compress_value) // 10, exif=exif_data)
            else:
                img.save(output_path, compress_level=(100 - compress_value) // 10)
    except OSError, ValueError:
        CTkMessagebox(title="ERROR06", message="Could not save file: " + os.path.basename(file), icon="cancel")
        return None
    finally:
        img.close()

    file_size_after = os.path.getsize(output_path)

    return {"size_before": file_size, "size_after": file_size_after, "renamed": was_renamed}

# Function that compresses photos
def compress():
    progress.set(0)
    # Checks if user gave any files
    if not selected_files:
        CTkMessagebox(title="ERROR01", message="No photos selected!", icon="cancel")
        return

    # Checks that a custom output folder, if set, still actually exists
    if settings.output_folder != "" and not os.path.isdir(settings.output_folder):
        CTkMessagebox(title="ERROR07", message="Output folder no longer exists! Please select it again in settings.", icon="cancel")
        return

    total_before = 0
    total_after = 0
    renamed = 0

    compress_value = int(quality.get())

    if settings.output_folder == "":
        output_folder_msg = CTkMessagebox(title="WARNING01", message="Output folder not specified! Do you want to continue?", icon="question", option_1="No", option_2="Yes")
        response = output_folder_msg.get()
        if response == "No": 
            CTkMessagebox(title="Aborted", message="Compression aborted.", icon="cancel")
            return

    lock_ui()
    used_paths = set()

    try:
        for i, file in enumerate(selected_files):
            result = compress_single_file(file, compress_value, used_paths)
            if result is None:
                continue

            file_labels[file].configure(text=f"{os.path.basename(file)} — {result['size_before'] / MB:.2f} MB → {result['size_after'] / MB:.2f} MB")

            total_before += result["size_before"]
            total_after += result["size_after"]
            if result["renamed"]:
                renamed += 1

            progress.set((i + 1) / len(selected_files))
            progress.update()
    finally:
        unlock_ui()

    # Calculating space
    if total_before == 0: return
    total_difference = (total_before - total_after) / MB
    total_difference_percent = (total_before - total_after) / total_before * 100

    before_space_lbl.configure(text=f"Before compression: {total_before / MB:.2f}MB")
    after_space_lbl.configure(text=f"New size: {(total_before / MB) - total_difference:.2f}MB")

    message = "Compression completed!\n" + f"Saved {total_difference:.2f} MB (decreased in size by {total_difference_percent:.1f}%)"
    if renamed > 0:
        message += f"\n{renamed} file(s) were renamed to avoid overwriting another compressed file."
    if settings.output_folder == "":
        message += "\nNo output folder was specified, so the compressed files were saved in the same folders as the original files."

    CTkMessagebox(title="Done", message=message, icon="check")

# Function that updates quality label
def update_label(value):
    quality_lbl.configure(text=f"Quality: {int(value)}")

# Function that shows settings window
def show_settings(app):
    global settings_win
    if settings_win is None or not settings_win.winfo_exists():
        settings_win = settings.open_settings(app)

# Function that clears whole list of selected files
def clear_list():
    global selected_files

    selected_files.clear()
    file_labels.clear()
    thumbnail_refs.clear()
    remove_buttons.clear()
    for widget in files_frame.winfo_children():
        widget.destroy()
    counter_lbl.configure(text="Selected files: 0")
    before_space_lbl.configure(text="Before: -")
    after_space_lbl.configure(text="New size: -")
    progress.set(0)

# Theme
ctk.set_appearance_mode(settings.appearance_mode)
ctk.set_default_color_theme("blue")

# Basic app structure
app = ctk.CTk()
app.title("SnapPress")

if platform.system() == "Windows":
    app.iconbitmap(utils.resource_path("assets/logo.ico"))
else:
    icon_img = PhotoImage(file=utils.resource_path("assets/logo.png"))
    app.icon_img = icon_img
    app.iconphoto(True, icon_img)

app.geometry("600x750")

# Settings
settings_img = Image.open(utils.resource_path("assets/settings.png"))
settings_icon = ctk.CTkImage(light_image=settings_img, dark_image=settings_img, size=(48, 48))
settings_img.close()
settings_button = ctk.CTkButton(app, image=settings_icon, text="", command=lambda: show_settings(app), width=40, fg_color=("#E5E5E5", "#313233"), hover_color=("#D0D0D0", "#404142"),)
settings_button.pack(padx=5, pady=5, anchor="e")

# Drag & Drop (also clickable)
drop_frame = ctk.CTkFrame(app, height=120, border_width=2)
drop_frame.pack(padx=20, pady=20, fill="x")

drop_label = ctk.CTkLabel(drop_frame, text="Click to select photos\nJPG, PNG, AVIF, WEBP", font=("Arial", 13))
drop_label.pack(expand=True, pady=40)

drop_frame.bind("<Button-1>", lambda e: select_photos())
drop_label.bind("<Button-1>", lambda e: select_photos())

# Frame with pictures
counter_frame = ctk.CTkFrame(app, fg_color="transparent")
counter_frame.pack(padx=20, pady=(10, 0), fill="x")

counter_lbl = ctk.CTkLabel(counter_frame, text="Selected files: 0", font=("Arial", 13, "bold"))
counter_lbl.pack(side="left")

clear_list_btn = ctk.CTkButton(counter_frame, text="Clear list", command=clear_list, width=80)
clear_list_btn.pack(side="right")

# Shows loaded photos
files_frame = ctk.CTkScrollableFrame(app, height=150)
files_frame.pack(padx=20, fill="x")

# Label that shows how compressed picture will get
quality_lbl = ctk.CTkLabel(app, text="Quality: 80", font=("Arial", 13))
quality_lbl.pack()

# Slider to decide how compress
quality = ctk.CTkSlider(app, from_=1, to=95, command=update_label)
quality.pack(padx=20, pady=10, fill="x")
quality.set(80)

# Box that shows how much space you save with compressing
stats_frame = ctk.CTkFrame(app, fg_color="transparent")
stats_frame.pack(padx=20, fill="x")

before_space_frame = ctk.CTkFrame(stats_frame, height=60, border_width=2)
before_space_frame.pack(side="left", expand=True, fill="x", padx=(0, 5))

before_space_lbl = ctk.CTkLabel(before_space_frame, text="Before: -", font=("Arial", 13))
before_space_lbl.pack(anchor="w", padx=10, pady=10)

after_space_frame = ctk.CTkFrame(stats_frame, height=60, border_width=2)
after_space_frame.pack(side="right", expand=True, fill="x", padx=(5, 0))

after_space_lbl = ctk.CTkLabel(after_space_frame, text="New size: -", font=("Arial", 13))
after_space_lbl.pack(anchor="w", padx=10, pady=10)

# Shows compress progress
progress = ctk.CTkProgressBar(app)
progress.pack(padx=20, pady=10, fill="x")
progress.set(0)

# Button to start compress
btn_compress = ctk.CTkButton(app, text="Compress and save", command=compress)
btn_compress.pack(pady=10)

ctk.CTkLabel(app, text="v1.12.1", text_color=("gray50", "gray60")).pack(padx=20, pady=(0, 5))

app.mainloop()