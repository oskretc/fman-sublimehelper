# SublimeHelper
[fman](https://fman.io) plugin to work with Sublime Text Editor

#Installation
1 Install using fman Install Plugin command
2 Modify the file __init__.py and change the **SUBLIMETEXTPATH** to match your system

# Usage
* Invoke command window with Ctrl+Shift+P/Cmd+Shift+P and type sublime

# Features
* Command: **Sublime open selected**:
  * 1 file selected, the file will be open in an existing window (same as F4 if Sublime text editor is selected)
  * Multiple files selected, the files will be open in a new window (if folder selected, folders will also be added)
* Command: **Sublime open current folder in new window**
  * The current folder will be added to a new Sublime text window and any selected files will be opened



# TODO
* Get Editor Path from Settings
* TODO: Check if quoting is working for other platforms