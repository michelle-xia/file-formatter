# file-formatter
Formats Microsoft Word files according to specifications

# Purpose
I was tired of formatting word document deliverables, so I decided to code my own automation tool to do the formatting.

# Usage
1) Clone the repository, update Word.in with what you want to name your formatted file, followed by a space, and the path you want to save the formatted file in.
The default directory is the current one.
2) If you have `make` installed, run `make file`. On Windows, you can install MinGW [here](https://sourceforge.net/projects/mingw/files/latest/download?source=files) and add "C:\MinGW\msys\1.0\bin" to your PATH. Select the PDF file with the requirements, and you've got your formatted document.
3) If you don't have `make` you can also run the program with `python3 format_file.py`. Type the name for your formatted file, space, path to save to. `./` is the current directory. Select the PDF file with the requiremnts.

# APIs
I am using the PDFMiner API for input instructions and a Microsoft Word API for the output template.
