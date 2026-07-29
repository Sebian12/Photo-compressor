# SnapPress

A desktop application for compressing JPEG, PNG, AVIF and WEBP photos without visible quality loss. Built with Python and customtkinter.

![Python](https://img.shields.io/badge/Python-3.14-blue) ![Pillow](https://img.shields.io/badge/Pillow-12.x-green) ![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)

<img width="200" height="250" alt="SnapPress GIF" src="https://github.com/user-attachments/assets/4de56762-34cd-43f4-98d9-06028ec15e57" />

## Features

- Batch compression (multiple files at once)
- Adjustable quality slider (1–95%)
- Progress bar with live feedback
- Savings summary (before / after)
- Saves compressed files next to originals — originals are never overwritten
- Settings menu with custom output folder and adjustable thumbnail size

## Screenshots

![Empty](assets/empty.png)
![Dark mode](assets/dark_mode.png)
![After compression](assets/one_file_comp.png)
![Multiple files](assets/multiple_files_comp.png)

## Requirements

- Python 3.10+
- Pillow

## Installation

### Universal (Windows, macOS, Linux)
1. Clone the repository:
```bash
git clone https://github.com/Sebian12/SnapPress.git
cd SnapPress
```

2. Install dependencies:
```bash
pip install Pillow customtkinter CTkMessagebox
```

3. Run the app:
```bash
python main.py
```

### Windows only

1. Download .exe file from current release or Apertix website.

## Usage

1. Click **Choose photos** to select files
2. Adjust the quality slider (default: 80%)
3. Click **Compress and save**
4. Compressed files are saved in the same folder as the originals with a `_compressed` suffix or saved in selected folder

## Roadmap

- [x] Switch from tkinter to customtkinter
- [x] Dark mode (1.2.0)
- [x] Settings menu (1.3.0)
- [x] Custom output folder (1.4.0)
- [x] Settings saver (1.5.0)
- [x] File counter (1.5.0)
- [x] Button to clear photo list or single photo (1.5.0)
- [x] Compressed file size next to file name (1.6.0)
- [x] Thumbnails of photos (1.7.0)
- [x] App logo (1.7.1)
- [x] User set thumbnail size (1.7.2)
- [x] Optimization (1.8.0)
- [x] EXIF metadata preservation (1.9.0)
- [x] Granular metadata control in settings (only GPS data checkbox) (1.10.0)
- [x] More metadata control in settings (1.11.0)
- [x] New file format support (1.12.0)
- [ ] Pack compressed photos to zip (1.13.0)
- [ ] Multithreading (planned)
- [ ] Drag & Drop support (planned)

## Part of the Apertix ecosystem

| App                                                                | Platform | Language |
|--------------------------------------------------------------------|----------|----------|
| [SnapPress](https://github.com/Sebian12/SnapPress)                 | Windows / Linux / Web | Python / JavaScript |
| [SnapPress Android](https://github.com/Sebian12/SnapPress-Android) | Android | Kotlin |
| [SnapRename](https://github.com/Sebian12/SnapRename)               | Windows | C# |
| SnapRename Android (planned)                                       | Android | Kotlin |

## Tech stack

- Python 3.14
- customtkinter — GUI
- Pillow — image processing
- CTkMessageBox

## License

MIT
