# RenewedWorldConverter
This a user-friendly Python-based GUI wrapper around the Java [LotrWorldConverter](https://github.com/mist475/LotrModConverter_Public/tree/dev) project (by Mist475) to allow users to update their worlds from the Minecraft LOTR: Legacy mod to LOTR: Renewed

LegacyWorldConverter-all.jar is an uber-jar with all required dependencies based on the latest code from Mist475's converter dev branch (as of 7/27/25).

Conversions.json is also based on his latest from that date.

## Features/Todo
- [X] Create initial GUI wrapper
- [X] Conversion correctly works in a Temp folder on Windows
- [X] Setup PyInstaller to make a complete Windows executable wrapper for this converter
- [X] Auto copy the converted Legacy world to the same directory as the Renewed world was in
- [X] Create an updated silent version of LegacyWorldConverter-all.jar that only prints out progress
- [ ] Add a progress bar that listens to the output
- [ ] Create an ExtendedConversions.json that adds support for Renewed Extended and include a checkbox to allow it to be used
- [ ] Add a Welcome menu that explains you will need to create a World in Renewed to use as the basis of your conversion, includes information about the authors, and has the Renewed Extended Team logo.
- [ ] Print the output to a log file in Temp
- [ ] Add support for CLI usage

## Installing packages & Running locally
After you have Python installed make sure you create your virtual environment and install the requirements:
```
python -m venv .venv
.venv\Scripts\activate  # (or source .venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
```

When developing/testing you can run it from outside the renewed_world_converter folder:

```python -m renewed_world_converter.__main__```

## Building executable with PyInstaller
For production version (user-friendly and no debugging)
```pyinstaller pyinstaller/RenewedWorldConverter.spec```

For debug version (testing when developing features)
```pyinstaller pyinstaller/RenewedWorldConverter_debug.spec```
