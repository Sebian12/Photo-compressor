# Changelog

## v1.11.0

### New Features
- Added granular EXIF metadata control: a new "More EXIF options" window (opened from Settings, enabled only while "Preserve EXIF metadata" is on) lets you selectively strip individual EXIF fields instead of an all-or-nothing choice — grouped into Location (GPS), Camera (make, model, lens make/model, exposure time, F-number, ISO, focal length), Date & Time (modified, original, digitized), Author (artist, copyright), and Software
- Turning off "Preserve EXIF metadata" now resets all individual field selections back to off, rather than remembering them for next time

### Maintenance
- `compress_single_file()` now builds EXIF data from a single consistent source (`img.getexif()`) instead of switching between raw EXIF bytes and a different object type depending on settings, which could silently produce inconsistent results
- Replaced the old standalone `remove_gps` setting with the unified `exif_remove` structure shared by all metadata fields; existing config files with the old setting are migrated automatically on first load
- Centralized the list of available EXIF fields, their tag IDs, and default state in `config.py` (`EXIF_FIELDS` / `DEFAULT_EXIF_REMOVE`) as a single source of truth

## v1.10.5

### Maintenance
- Extracted duplicated `resource_path()` from `main.py` and `settings.py` into a shared `utils.py`
- Added `save_settings()` helper in `settings.py` to replace repeated `config.save_config(...)` calls with all five arguments
- Renamed `b_mode` to `appearance_mode` for naming consistency
- Renamed `qualityLbl` to `quality_lbl` to match snake_case convention used elsewhere
- Documented ERROR0x/WARNING0x numbering scheme
- Split `compress()` into `lock_ui()`, `unlock_ui()`, and `compress_single_file()` for readability

### Improvements
- `WARNING01` (no output folder set) is now a Yes/No confirmation instead of a plain info message; declining aborts the compression with a dedicated messagebox
- Completion summary now notes when files were saved next to the originals because no output folder was set

## v1.10.4

### Bugfixes
- Settings button and photo drop area are now disabled while a compression batch is running, preventing settings or file list changes from producing inconsistent results mid-batch

### Reverted
- Reverted an attempt to scope the Settings window's "always on top" behavior to just the main window instead of the whole desktop — caused display issues, so the previous behavior was restored

### Improvements
- Version label at the bottom of the main window is now a muted gray instead of full-brightness text
- Added `CHANGELOG.md` to track release history directly in the repo
- Various README.md updates

## v1.10.3

### Features
- Added app logo to the settings window
- Added version label to the bottom of the main window

## v1.10.2

### Bugfixes
- Fixed `preserve_exif` setting having no effect on compression — EXIF metadata (including GPS) was preserved regardless of the "Preserve EXIF metadata" toggle, and `remove_gps` stayed enabled internally after disabling EXIF preservation
- Fixed compressed files silently overwriting each other when two selected files had the same name but came from different folders
- Fixed unhandled exception crashing the whole batch when a file failed to save — output folder is now validated before compression starts
- Fixed file list and buttons staying interactive during compression, which could cause files to be silently skipped if the list changed mid-run
- Fixed orphaned frame widget left in memory when a thumbnail failed to load
- Fixed `save_config()` crashing on write errors instead of failing gracefully

## v1.10.1

### Features
- Changed app logo
- Updated README.md

### Known limitations
- Logo might not be visible while using dark mode
- Logo doesn't show when downloading. Creating a copy or a shortcut to the app changes the logo

## v1.10.0

### Features
- Added "Preserve EXIF metadata" toggle in settings
- Added "Remove GPS data" checkbox in settings (active only when EXIF preservation is enabled)
- GPS tag (34853) is now stripped from compressed JPG when "Remove GPS data" is enabled

### Bugfixes
- Fixed `FileNotFoundError` — `os.path.getsize()` was called before the `os.path.exists()` check
- Fixed `before_space_lbl` and `after_space_lbl` not resetting when clearing the list
- Fixed `preserve_exif` and `remove_gps` not being restored from config on app startup
- Fixed thumbnail size slider not restoring saved value on settings open (`thumb_size` saved as float, now cast to int)

### Known limitations
- EXIF metadata preservation not supported for PNG files

### Notes
- This and the next release (1.11.0) won't contain native Ubuntu-based or Fedora Linux binaries
- Mid patches like 1.x.1 etc. won't be released as Linux binaries

## v1.9.0

### Features
- EXIF metadata preservation for JPG/JPEG files during compression
- File picker and output folder dialog now start from `/home` on Linux instead of `/` for better UX

### Bugfixes
- Fixed missing `f` prefix in WARNING02 message — `{skipped}` was not interpolated
- Fixed `.jpg`/`.jpeg` files not visible in file picker on Linux — "All Files" is now the default filter on Linux

### Known limitations
- EXIF metadata preservation not supported for PNG files

## v1.8.6

### Features
- Replaced tkinter messagebox with CTkMessagebox — dialogs now follow the app theme (dark/light mode)

### Maintenance
- Updated screenshots in `assets/`
- Updated README — added CTkMessagebox and customtkinter to Requirements and Installation sections

## v1.8.5

### Bugfixes
- Fixed memory leak in `remove_file()` — `thumbnail_refs` was not cleared when removing a single file
- Fixed `settings_win == None` changed to `settings_win is None` (proper Python `None` comparison)
- Fixed `app` parameter in `show_settings()` renamed to `root` to avoid shadowing outer scope variable
- Fixed `icon_img` garbage collection issue on Linux — stored as `app.icon_img` to prevent premature cleanup
- Fixed `TypeError: open_settings() takes 0 positional arguments but 1 was given`

## v1.8.4

### Features
- Added native Linux binary for Fedora Linux

### Notes
- App icon works correctly on Fedora Linux

## v1.8.3

### Bugfixes — Linux
- Fixed `ImportError: PIL.Image and PIL.ImageTk couldn't be imported` in compiled Linux binary — added `--hidden-import PIL._tkinter_finder` and `--hidden-import PIL.ImageTk` to the PyInstaller build command
- Removed broken app icon (`iconphoto`) on Linux causing `_tkinter.TclError: not a photo image` on startup

### Bugfixes — Windows
- Fixed settings window closing unexpectedly when toggling dark/light mode (removed `transient()` + `WM_DELETE_WINDOW` combination causing conflict with customtkinter theme rebuild)

### Maintenance
- Removed redundant `if/else: pass` blocks in `compress()`

### Known limitations — Linux
- Output folder dialog may appear behind the settings window (`-topmost` removed alongside `transient`)
- App icon is not displayed on Linux (removed due to `PhotoImage`/`iconphoto` incompatibility, root cause not yet identified)

## v1.8.2 (Linux only)

### Bugfixes
- Fixed `ImportError: PIL.Image and PIL.ImageTk couldn't be imported` in compiled Linux binary

### Other
- Added screenshots from the Linux app

## v1.8.1

### Features
- Added native Linux binary (built and tested on Zorin OS 18.1, Ubuntu-based)
- Cross-platform icon handling: `.ico` on Windows via `iconbitmap`, `.png` on Linux via `iconphoto`

### Bugfixes
- Fixed settings window appearing behind the output folder dialog (`transient(app)` instead of `topmost`)

### Maintenance
- Updated `.gitignore`
- Updated README with Linux installation instructions and a Native Linux Support section

### Known limitations
- Linux binary may not work on distributions with an older glibc version or on non-glibc systems (e.g. Alpine)
- May have issues on pure Wayland sessions without XWayland
- App icon does not appear in dock/launcher on Linux (requires a `.desktop` file, not yet implemented)

## v1.8.0

### Improvements
- Code cleanup: removed redundant `if/else: pass` blocks
- Added `MB` constant to replace repeated `1024 * 1024`
- Reduced duplicate `os.path.getsize()` calls in `compress()`
- Unified naming convention to snake_case in `settings.py`
- `thumbnail_refs` now cleared in `clear_list()`

### Bugfixes
- Fixed `config.json` path resolution after compiling to `.exe`
- Added `WM_DELETE_WINDOW` handler in settings window to ensure config is saved on close

## v1.7.3

### Bugfixes
- Fixed `KeyError: 'thumb_size'` when loading old or missing `config.json`
- Fixed `UnboundLocalError` in `load_config()` — `json.load()` was called outside the `with` block

## v1.7.2

### Notes
- Repository name change
- **Forgot to push before tagging this release — the source code for this tag is actually still v1.7.1's. Don't use the source from this release.**

### Features
- Added user-set thumbnail size

## v1.7.1

### Bugfixes
- Added app icon (`logo.ico`) to window title bar and taskbar
- Fixed icon path compatibility between script and compiled `.exe`

## v1.7.0

### Features
- Added thumbnails next to file names in the list
- Updated roadmap in README.md

### Bugfixes
- Fixed progress bar not resetting on new compression
- Fixed thumbnail label reference not stored
- Added exception handling in `select_photos()`
- Fixed output folder no longer showing a confirmation dialog when no folder was selected

## v1.6.0

### Features
- Added file size before and after compression next to file name in the list

### Bugfixes
- Fixed `file_labels` dictionary now cleared on `clear_list()` and `remove_file()`

## v1.5.1

### Bugfixes
- Fixed `config.json` key mismatch between save and load (`appearance_mode` → `b_mode`)
- Fixed `row.pack()` called twice in `select_photos`
- Removed unused global `photos_counter` variable
- Fixed output folder warning now shows once before compression instead of for each file
- Fixed `load_config` now handles corrupted `config.json` with `try/except`

## v1.5.0

### Features
- Added settings saver for both theme and output folder
- Added file counter
- Added button to clear all images from the list, and buttons to remove only one

### Bugfixes
- Fixed bug with `.png` compressing — it didn't always work
- Prevented duplicate files from being added to the list
- Removed unnecessary import from `main`
- Unsupported file no longer clears the entire list during compression

## v1.4.2
- Added verification to safely skip missing files during the compression process

## v1.4.1

### Bugfixes
- Fixed bugs found in v1.4.0
- Minor fixes in README.md and in the UI

## v1.4.0

### Features
- Added custom folder output

### Known limitations
- You don't get notified if a photo is compressed — patched in v1.4.1
- When you set an output folder, close and reopen the settings menu, the output folder resets. Doesn't affect the program — patched in v1.4.1

## v1.3.4

### Bugfixes
- Fixed bug with dark mode switch — when you changed theme to dark mode, closed the settings menu and reopened it, the switch reset

## v1.3.3

### Bugfixes
- Added exception handling for when trying to select a different, unsupported file type

## v1.3.2

### Bugfixes
- Fixed "divide by zero" error that could occur when compressing without selecting files

## v1.3.1

### Bugfixes
- Fixed bug where you could open multiple settings menus at once

## v1.3.0

### Features
- Added settings menu
- Moved dark mode toggle into the settings menu

## v1.2.0

### Features
- Added dark mode

## v1.1.2
- Added `.exe` file

## v1.1.1
- Changed what the box on the bottom shows

## v1.1.0

### Features
- Added screenshots to README
- Updated tech stack (customtkinter)

## v1.0.0

### Features
- Select multiple photos (JPG, PNG)
- Adjustable quality slider (1–95%)
- Progress bar during compression
- Saves compressed files next to originals
- Shows how much space was saved (MB and %)