import os

from api.lib.test_file_detector.fileAnalysis import test_include, test_keyword
from api.lib.test_file_detector.utilities import lookup_generator, tech_lookup_generator

BASE_PATH = os.path.dirname(os.path.realpath(__file__))


class TestDetector:
    def __init__(self):
        self.keyword_lookup = lookup_generator(BASE_PATH + "/keywords.txt")  # keywords
        self.tech_lookup = tech_lookup_generator(
            BASE_PATH + "/testingTechnologiesFixed3.csv"
        )  # testtechs

    def get_file_contents(self, file_path):
        file_contents = ""
        opened_file = open(file_path, "r", encoding="latin-1")

        for line in opened_file:
            file_contents += line
            file_contents += "\n"

        opened_file.close()

        return file_contents

    def get_file_extension(self, file_path):
        return file_path.rpartition(".")[-1]

    def test_search(self, file_path):

        file_extension = self.get_file_extension(file_path)

        file_contents = self.get_file_contents(file_path)

        # verifica se o arquivo possui o import de um framework de teste conhecido
        has_test_import = test_include(self.tech_lookup, file_extension, file_contents)

        # verifica se o arquivo possui a chamada de funcao de um framework de teste conhecido
        has_test_call = test_keyword(self.keyword_lookup, file_extension, file_contents)

        # caso o arquivo tenha o import de teste E a chamada de função de teste, é considerado um arquivo de teste
        is_test_file = has_test_import + has_test_call == 2

        return is_test_file
