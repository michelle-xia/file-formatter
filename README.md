# file-formatter
Formats Microsoft Word files according to specifications

# Purpose
I was tired of formatting word document deliverables, so I decided to code my own automation tool to do the formatting.

# Usage
1) Clone the repository with `git clone https://github.com/michelle-xia/file-formatter.git` update [WordDoc.in](WordDoc.in) with what you want to name your formatted file, followed by a space, and the path you want to save the formatted file in. Check [WordDoc.in](WordDoc.in) for an example. The default directory is the current one.

2) Install the libraries with pip (see below).

3) If you have `make` installed, run `make file`. On Windows, you can install MinGW [here](https://sourceforge.net/projects/mingw/files/latest/download?source=files) and add `C:\MinGW\msys\1.0\bin` to your PATH. After you run `make file` select the PDF file with the requirements, and you've got your formatted document.

4) If you don't have `make` you can also run the program with `python3 format_file.py`. Type the name for your formatted file **with the .docx** (don't forget to include this), space, path to save to. `./` is the current directory. As an example: ```Formatted.docx ./``` Select the PDF file with the requirements.

# Dependencies
I am using PDFMiner for input instructions and python-docx for the output template. They can be installed with the following commands:
```pip install pdfminer```
```pip install python-docx```
