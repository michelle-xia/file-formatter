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
    """This function looks through a data list and returns a list with requirement keywords"""
    return [[a_list[i - 2], a_list[i - 1], a_list[i], a_list[i + 1], a_list[i + 2]] for i in range(
        len(a_list)) if i + 2 < len(a_list) and a_list[i] in requirements]


def get_specs(a_list):
    """This function works with parse_spects to separate individual elements within a spec list"""
    for i in range(len(a_list)):
        a_list[i] = [word.split("-") for word in a_list[i]]

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
    # look for 'margins'
    try:
        margin_ind = spec_list.index('margins')
    except ValueError:
        try:
            # look for 'margin'
            margin_ind = spec_list.index('margin')
        except ValueError:
            return -1

    return find_dict_value(spec_list, margin_ind, "float")


def find_number_pages(spec_list):
    """This function returns the page requirements, assuming you are ambitious and write the maximum amount or -1"""
    spec_list = get_specs(parse_specs(spec_list))
    try:
        page_ind = spec_list.index('pages')
    except ValueError:
        return -1

    return find_dict_value(spec_list, page_ind, "int")


def find_spacing(spec_list):
    """This function returns spacing requirements or -1"""
    spacing_list = ['double', 'single', '1.5']
    # look for 'spaced' and 'spacing'
    try:
        space_ind = spec_list.index('spaced')
    except ValueError:
        try:
            space_ind = spec_list.index('spacing')
        except ValueError:
            return "-1"

    # look at element before for spacing specification
    if space_ind > 0:
        try:
            if spec_list[space_ind - 1] in spacing_list:
                if spec_list[space_ind - 1] == "1.5":
                    return 'one_point_five'
                return spec_list[space_ind - 1]
        except ValueError:
            pass
    # look at element after for spacing specification
    try:
        if spec_list[space_ind + 1] in spacing_list:
            if spec_list[space_ind + 1] == "1.5":
                return 'one_point_five'
            return spec_list[space_ind + 1]
    except ValueError:
        return "-1"


def find_font(spec_list):
    """This function returns font requirements or -1"""
    font_list = ['arial', 'calibri', 'cambria', 'helvetica', 'times', 'new', 'roman', 'verdana']
    try:
        font_ind = spec_list.index('type')
    except ValueError:
        try:
            font_ind = spec_list.index('font')
        except ValueError:
            return "-1"
    if font_ind > 0:
        if spec_list[font_ind - 1] in font_list:
            return spec_list[font_ind - 1]
    try:
        if spec_list[font_ind + 1] in font_list:
            return spec_list[font_ind + 1]
    except ValueError:
        pass

    return "-1"


def find_size(spec_list):
    """This function returns font size requirements or -1"""
    spec_list = get_specs(parse_specs(spec_list))
    try:
        size_ind = spec_list.index('point')
    except ValueError:
        try:
            size_ind = spec_list.index('size')
        except ValueError:
            return "-1"

    # more ambiguity with size specification wording, look for two before
    val = find_dict_value(spec_list, size_ind, "int")
    if val == -1:
        val = find_dict_value(spec_list, size_ind - 1, "int")
    if val == -1:
        return "-1"
    return val


def find_dict_value(spec_list, ind, val_type=""):
    """This function returns the requirement value found to the left or right in spec_list or -1"""
    # look at element before for specification
    if ind > 0:
        try:
            if val_type == "int":
                return int(spec_list[ind - 1])
            elif val_type == "float":
                return float(spec_list[ind - 1])
        except ValueError:
            pass
    # look at element after for specification
    try:
        if val_type == "int":
            return int(spec_list[ind + 1])
        elif val_type == "float":
            return float(spec_list[ind + 1])
    except ValueError:
        return -1


def print_words(a_list):
    """This function prints the elements in a 2d list"""
    for element in a_list:
        print(element)


def main():
    file_to_parse = 'UGCAF2020Assignment1.pdf'
    print(parse_requirements(file_to_parse))


if __name__ == "__main__":
    main()

