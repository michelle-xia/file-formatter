from docx import Document
from docx.shared import Pt
from docx.shared import Inches
from docx.enum.text import WD_LINE_SPACING
import os


def create_doc(spec_dict, doc_name="", path_to_doc=""):
    """This function creates a word document formatted with the specifications"""
    document = Document()

    styles = document.styles['Normal']
    font = styles.font

    # set font
    if spec_dict['font'] != "-1":
        font.name = spec_dict['font'].capitalize()

    # set size
    if str(spec_dict['size']) != "-1":
        font.size = Pt(spec_dict['size'])

    # set margins
    if spec_dict['margins'] != -1:
        sections = document.sections
        for section in sections:
            section.top_margin = Inches(spec_dict['margins'])
            section.bottom_margin = Inches(spec_dict['margins'])
            section.left_margin = Inches(spec_dict['margins'])
            section.right_margin = Inches(spec_dict['margins'])

    paragraph = document.add_paragraph()

    # set spacing
    if spec_dict['spacing'] != "-1":
        if spec_dict['spacing'] == 'single':
            paragraph.line_spacing_rule = WD_LINE_SPACING.SINGLE
        elif spec_dict['spacing'] == 'double':
            paragraph.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        elif spec_dict['spacing'] == 'one_point_five':
            paragraph.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    paragraph.style = document.styles['Normal']

    # create pages
    if spec_dict['pages'] != -1:
        for i in range(spec_dict['pages'] - 1):
            document.add_page_break()

    # save doc
    if doc_name != "" and path_to_doc != "":
        path_to_doc = os.path.join(path_to_doc, doc_name)
        document.save(path_to_doc)
    elif path_to_doc != "":
        path_to_doc = os.path.join(path_to_doc, 'Formatted.docx')
        document.save(path_to_doc)
    elif doc_name != "":
        document.save(doc_name)
    else:
        document.save('Formatted.docx')
