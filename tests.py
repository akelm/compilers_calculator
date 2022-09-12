import unittest
from parameterized import parameterized

from functions import calculate, ParserError, LexerError
from pyparsing_reference import parse_expr

correct_expression_list = {
    '2+3/4',
    ' 2+3',
    '  2 +  3  ',
    ' 2 + 3 ',
    '-2+77',
    '1	/	33   ',
    '-(-3)+5',
    '((3))',
    '8*6/4-1',
    '8/3/2',
    "(3 * 16 + 3 * 1)",
    "(6 + 16) / 16",
    "(8 * 10)",
    "(5 * 12 / 16)",
    "6 * 3 + 14 + 0",
    "13 + 15 - 1",
    "19 + (8 / 8)",
    "2*3-6",
    "78/8-9",
    "(23)",
    "86 + 84 + 87 / (96 - 46) / 59",
    "((((49)))) + ((46))",
    "76 + 18 + 4 - (98) - 7 / 15",
    "(((73)))",
    "(55) - (54) * 55 + 92 - 13 - ((36))",
    "(78) - (7 / 56 * 33)",
    "(81) - 18 * (((8)) * 59 - 14)",
    "(((89)))",
    "(59)",
    "(12 + 3 - 5)",
    "(4 * 0 / 4)",
    "1 - 18 / (3 * 15)",
}

incorrect_expression_dict = {
    '': ParserError,
    '3---4': ParserError,
    '3+++4': ParserError,
    '(3)(2)': ParserError,
    '(3)+2)': ParserError,
    '()': ParserError,
    '/33': ParserError,
    '-abs ': LexerError,
    '2 +/ 3+ 7': ParserError,
    '-+2+7': ParserError,
    '--3+5': ParserError,
    "2(85+96)*12-96": ParserError,

}


class TestEvaluation(unittest.TestCase):

    @parameterized.expand(correct_expression_list)
    def test_evaluation_correct(self, text: str):
        res = calculate(text)
        res_ref = parse_expr(text)
        self.assertEqual(res_ref, res)

    @parameterized.expand(incorrect_expression_dict.items())
    def test_evaluation_incorrect(self, text: str, exc: Exception):
        with self.assertRaises(Exception):
            parse_expr(text)
            self.fail('Reference function did not fail!')
        with self.assertRaises(exc):
            calculate(text)