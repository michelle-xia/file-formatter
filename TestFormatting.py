#!/usr/bin/env python3

from unittest import main, TestCase
from FormatFile import format_read, run_file_formatter
from ParseRequirements import parse_requirements, read_pdf, clean_list,  parse_specs, create_dict, \
    find_margins, find_number_pages, find_spacing, find_font, find_size, get_word_index, find_dict_value
from CreateDoc import create_doc


class TestFormatting(TestCase):

    def test_read(self):
        s = "file.docx ./"
        i, j = format_read(s)
        self.assertEqual(i, "file.docx")
        self.assertEqual(j, "./")

    def test_parse_requirements(self):
        file_to_parse = 'Tester.pdf'
        tester_requirements = {'margins': 2, 'pages': 3, 'spacing': 'double', 'size': 15, 'font': 'Times New Roman'}
        assert parse_requirements(file_to_parse) == tester_requirements


if __name__ == "__main__":
    main()
