from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io

requirements = ['margin', 'margins', 'spacing', 'font', 'size', 'pages', 'spaced']


def pdf_parser(file_name):
    """This function takes in a pdf file and returns a list of specifications within the pdf file"""
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
    get_specs(data_list)


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

    return [val[i] for val in a_list for i in range(len(val))]



def print_words(a_list):
    for word in a_list:
        print(word)


def main():
    file_to_parse = 'file.pdf'
    pdf_parser(file_to_parse)


if __name__ == "__main__":
    main()

