#!/usr/bin/env python3

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
    if spec_dict['font'] is not None:
        font.name = spec_dict['font'].capitalize()
    else:
        font.name = 'Calibri'

    # set size
    if spec_dict['size'] is not None:
        font.size = Pt(spec_dict['size'])

    # set margins
    if spec_dict['margins'] is not None:
        sections = document.sections
        for section in sections:
            section.top_margin = Inches(spec_dict['margins'])
            section.bottom_margin = Inches(spec_dict['margins'])
            section.left_margin = Inches(spec_dict['margins'])
            section.right_margin = Inches(spec_dict['margins'])
    else:
        sections = document.sections
        for section in sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)

    paragraph = document.add_paragraph(str(spec_dict))
    paragraph.style = document.styles['Normal']
    paragraph_format = paragraph.paragraph_format

    # set spacing
    if spec_dict['spacing'] is not None:
        if spec_dict['spacing'] == 'single':
            paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        elif spec_dict['spacing'] == 'double':
            paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        elif spec_dict['spacing'] == '1.5':
            paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    # create pages
    if spec_dict['pages'] is not None:
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
