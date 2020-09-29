from src.parse_requirements import parse_requirements
from src.create_formatted_doc import create_doc


def run_file_formatter(file_to_parse, word_doc_name="", path_to_word_doc=""):
    requirements_dict = parse_requirements(file_to_parse)
    create_doc(requirements_dict, word_doc_name, path_to_word_doc)


if __name__ == "__main__":
    run_file_formatter("file.pdf")
