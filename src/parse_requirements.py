from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io

requirements = ['margin', 'margins', 'spacing', 'font', 'size', 'pages', 'spaced']


def pdf_parser(file_name):
    """This function takes in a pdf file and returns a dictionary of the specifications within the pdf file"""
    data = ""
    fp = open(file_name, 'rb')

    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    laparams = LAParams()

    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    # create a pdf interpreter object
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # parse each page contained in the document
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data = retstr.getvalue()

    # prepare data for processing
    data = data.lower()
    data_list = data.split(" ")
    data_list = clean_list(data_list)
    data_list = parse_specs(data_list)
    spec_list = get_specs(data_list)
    print(spec_list)
    create_dict(spec_list)


def clean_list(a_list):
    remove_words = ['', '.', '•']
    a_list = [word.strip() for word in a_list]

    return [word.strip(".\"\':,“”()") for word in a_list if word not in remove_words]


def parse_specs(a_list):
    return [[a_list[i - 2], a_list[i - 1], a_list[i], a_list[i + 1], a_list[i + 2]] for i in range(
        len(a_list)) if i + 2 < len(a_list) and a_list[i] in requirements]


def get_specs(a_list):
    for i in range(len(a_list)):
        a_list[i] = [word.split("-") for word in a_list[i]]

    a_list = [item[i] for item in a_list for i in range(len(item))]

    return [val[i].strip('\"\'') for val in a_list for i in range(len(val))]


def create_dict(spec_list):
    """This function returns a dictionary from the requirements in spec_list"""
    spec_dict = dict()
    spec_dict['margins'] = find_margins(spec_list)
    print(spec_dict)


def find_margins(spec_list):
    # look for 'margins'
    margin_ind = spec_list.index('margins')

    # look for 'margin'
    if margin_ind == -1:
        margin_ind = spec_list.index('margin')

    if margin_ind == -1:
        return -1

    # look at element before for margin specification
    if margin_ind > 0:
        try:
            return float(spec_list[margin_ind - 1])
        except ValueError:
            pass
    # look at element after for margin specification
    try:
        return float(spec_list[margin_ind + 1])
    except ValueError:
        return -1


def print_words(a_list):
    for word in a_list:
        print(word)


def main():
    file_to_parse = 'file.pdf'
    pdf_parser(file_to_parse)


if __name__ == "__main__":
    main()

