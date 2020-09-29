from parse_requirements import parse_requirements
from create_formatted_doc import create_doc
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def format_read(r):
    a, b = r.strip().split()
    return a, b


def run_file_formatter(r):
    # load pdf requirements file
    Tk().withdraw()
    file_to_parse = askopenfilename()

    # get requirements from file
    requirements_dict = parse_requirements(file_to_parse)
    doc_name = ""
    doc_path = ""
    for s in r:
        doc_name, doc_path = format_read(s)

        # create formatted document
        create_doc(requirements_dict, doc_name, doc_path)


if __name__ == "__main__":
    run_file_formatter(sys.stdin)
