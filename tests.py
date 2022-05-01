import unittest
from typing import Union

from parameterized import parameterized

from check_string import check_string, calculate_value
import re

pattern = re.compile(r'^-?\s*\d+\s*((\+|-|\*|/)\s*\d+\s*)*$')

expression_dict = {
    '2+3/4': 5 / 4,
    ' 2+3': 5,
    '  2 +  3  ': 5,
    ' 2 + 3 ': 5,
    '-2+77': 75,
    '1\t/\t33   ': 1 / 33,
    '/33': "error",
    "-abs ": "error",
    "2 +/ 3+ 7": "error",
    "-+2+7": "error",
    "8*6/4-1": 11,
    "--3+5":"error"
}


class TestParser(unittest.TestCase):

    @parameterized.expand(expression_dict.keys())
    def test_correctness(self, text: str):
        result = 'A' if re.match(pattern, text) else 'N'
        self.assertEqual(result, check_string(text), "text: %s " % text)

    @parameterized.expand(expression_dict.items())
    def test_evaluation(self, text: str, value: Union[float, str]):
        self.assertEqual(value, calculate_value(text), "text: %s " % text)
