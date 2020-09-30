#!/usr/bin/env python3

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io

requirements = ['margin', 'margins', 'spacing', 'font', 'size', 'pages', 'spaced']


def parse_requirements(file_name, pages_to_parse=0):
    """This function takes in a pdf file and returns a dictionary of the specifications within the pdf file"""
    data_list = read_pdf(file_name, pages_to_parse)

    # create dictionary with specifications
    return create_dict(data_list)


def read_pdf(file_name, pages_to_parse=0):
    """This function takes in a pdf file and returns a list with all the words"""
    data = ""
    fp = open(file_name, 'rb')

    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    laparams = LAParams()

    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    # create a pdf interpreter object
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    if pages_to_parse == 0:
        # parse each page contained in the document
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
            data = retstr.getvalue()
    else:
        for page in PDFPage.get_pages(fp, None, pages_to_parse):
            interpreter.process_page(page)
            data = retstr.getvalue()

    # prepare data for processing
    data = data.lower()
    data_list = data.split(" ")
    return clean_list(data_list)


def clean_list(a_list):
    """This function removes blank lines and leading and trailing characters"""
    remove_words = ['', '.', '•']
    a_list = [word.strip() for word in a_list]

    return [word.strip(".\"\':,“”()") for word in a_list if word not in remove_words]


def parse_specs(a_list):
    """This function looks through a data list and returns a list with snippets around the requirement keyword"""
    # extract requirement phrases
    a_list = [[a_list[i - 2], a_list[i - 1], a_list[i], a_list[i + 1], a_list[i + 2]] for i in range(
        len(a_list)) if i + 2 < len(a_list) and a_list[i] in requirements]

    # extract individual elements
    for i in range(len(a_list)):
        a_list[i] = [word.split("-") for word in a_list[i]]

    # convert to 1d list
    a_list = [item[i] for item in a_list for i in range(len(item))]
    return [val[i].strip('\"\'') for val in a_list for i in range(len(val))]


def create_dict(spec_list):
    """This function returns a dictionary from the requirements in spec_list"""
    spec_dict = dict()
    spec_dict['margins'] = find_margins(spec_list)  # get margins
    spec_dict['pages'] = find_number_pages(spec_list)  # get pages
    spec_dict['spacing'] = find_spacing(spec_list)  # get spacing
    spec_dict['size'] = find_size(spec_list)  # get size
    spec_dict['font'] = find_font(spec_list)  # get font
    return spec_dict


def find_margins(spec_list):
    """This function returns the margin specifications or -1"""
    margin_ind = get_word_index(spec_list, "margins", "margin")

    # more ambiguity with margin specification wording, look for two before and after
    val = find_dict_value(spec_list, margin_ind, "float")
    if val is None:
        val = find_dict_value(spec_list, margin_ind - 1, "float")
        if val is None:
            val = find_dict_value(spec_list, margin_ind + 1, "float")
    return val


def find_number_pages(spec_list):
    """This function returns the page requirements, assuming you are ambitious and write the maximum amount or -1"""
    spec_list = parse_specs(spec_list)
    page_ind = get_word_index(spec_list, "pages")

    return find_dict_value(spec_list, page_ind, "int")


def find_spacing(spec_list):
    """This function returns spacing requirements or -1"""
    spacing_list = ['double', 'single', '1.5']
    space_ind = get_word_index(spec_list, "spaced", "spacing")
    spacing = find_dict_value(spec_list, space_ind, "", spacing_list)
    if spacing is None:
        spacing = find_dict_value(spec_list, get_word_index(spec_list, "spacing"), "", spacing_list)
    return spacing


def find_font(spec_list):
    """This function returns font requirements or -1"""
    font_list = ['arial', 'calibri', 'cambria', 'helvetica', 'times', 'new', 'roman', 'verdana']
    times_new_roman = ['times', 'new', 'roman']

    font_ind = get_word_index(spec_list, "type", "font")
    font = find_dict_value(spec_list, font_ind, "", font_list)
    if font is None:
        font = find_dict_value(spec_list, get_word_index(spec_list, 'font'), "", font_list)
    if font in times_new_roman:
        font = 'Times New Roman'
    return font


def find_size(spec_list):
    """This function returns font size requirements or -1"""
    spec_list = parse_specs(spec_list)
    size_ind = get_word_index(spec_list, "point", "size")

    # more ambiguity with size specification wording, look for two before
    val = find_dict_value(spec_list, size_ind, "int")
    if val is None:
        val = find_dict_value(spec_list, size_ind - 1, "int")
    if val is None:
        val = find_dict_value(spec_list, get_word_index(spec_list, "size"), "int")
        if val is None:
            val = find_dict_value(spec_list, get_word_index(spec_list, "size") - 1, "int")
    return val


def get_word_index(spec_list, w1, w2=""):
    try:
        return spec_list.index(w1)
    except ValueError:
        try:
            return spec_list.index(w2)
        except ValueError:
            return -1


def find_dict_value(spec_list, ind, val_type="", word_bank=[]):
    """This function returns the requirement value found to the left or right in spec_list or -1"""
    # look at element before for specification
    try:
        if val_type == "int":
            return int(spec_list[ind - 1])
        elif val_type == "float":
            return float(spec_list[ind - 1])
        elif len(word_bank) > 0:
            if spec_list[ind - 1] in word_bank:
                return spec_list[ind - 1]
    except ValueError:
        pass
    # look at element after for specification
    try:
        if val_type == "int":
            return int(spec_list[ind + 1])
        elif val_type == "float":
            return float(spec_list[ind + 1])
        elif len(word_bank) > 0:
            if spec_list[ind + 1] in word_bank:
                return spec_list[ind + 1]
    except ValueError:
        return None
