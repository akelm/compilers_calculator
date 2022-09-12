import operator
import string
from enum import Enum, auto


class TokenTypes(Enum):
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    START = auto()
    END = auto()
    EMPTY = auto()
    UNARY_MINUS = auto()


op_dict_str = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv, }

assign_dict = {"+": TokenTypes.PLUS, "-": TokenTypes.MINUS, "*": TokenTypes.MUL, "/": TokenTypes.DIV,
               "(": TokenTypes.LEFT_BRACKET, ")": TokenTypes.RIGHT_BRACKET}

whitespace = " \t"

all_chars = "".join(assign_dict.keys()) + whitespace + string.digits


class SymbolTypes(Enum):
    EXPRESSION = auto()
    EXPRESSION_PRIM = auto()
    TERM = auto()
    TERM_PRIM = auto()
    FACTOR = auto()
    UNSIGNED_FACTOR = auto()
    EMPTY = auto()


parse_table = {(SymbolTypes.EXPRESSION, TokenTypes.MINUS): [SymbolTypes.TERM, SymbolTypes.EXPRESSION_PRIM],
               (SymbolTypes.EXPRESSION, TokenTypes.LEFT_BRACKET): [SymbolTypes.TERM, SymbolTypes.EXPRESSION_PRIM],
               (SymbolTypes.EXPRESSION, TokenTypes.NUMBER): [SymbolTypes.TERM, SymbolTypes.EXPRESSION_PRIM],

               (SymbolTypes.EXPRESSION_PRIM, TokenTypes.PLUS): [TokenTypes.PLUS, SymbolTypes.TERM,
                                                                SymbolTypes.EXPRESSION_PRIM],
               (SymbolTypes.EXPRESSION_PRIM, TokenTypes.MINUS): [TokenTypes.MINUS, SymbolTypes.TERM,
                                                                 SymbolTypes.EXPRESSION_PRIM],
               (SymbolTypes.EXPRESSION_PRIM, TokenTypes.RIGHT_BRACKET): [SymbolTypes.EMPTY],
               (SymbolTypes.EXPRESSION_PRIM, TokenTypes.END): [SymbolTypes.EMPTY],

               (SymbolTypes.TERM, TokenTypes.MINUS): [SymbolTypes.FACTOR, SymbolTypes.TERM_PRIM],
               (SymbolTypes.TERM, TokenTypes.LEFT_BRACKET): [SymbolTypes.FACTOR, SymbolTypes.TERM_PRIM],
               (SymbolTypes.TERM, TokenTypes.NUMBER): [SymbolTypes.FACTOR, SymbolTypes.TERM_PRIM],

               (SymbolTypes.TERM_PRIM, TokenTypes.PLUS): [SymbolTypes.EMPTY],
               (SymbolTypes.TERM_PRIM, TokenTypes.MINUS): [SymbolTypes.EMPTY],
               (SymbolTypes.TERM_PRIM, TokenTypes.RIGHT_BRACKET): [SymbolTypes.EMPTY],
               (SymbolTypes.TERM_PRIM, TokenTypes.END): [SymbolTypes.EMPTY],
               (SymbolTypes.TERM_PRIM, TokenTypes.MUL): [TokenTypes.MUL, SymbolTypes.FACTOR, SymbolTypes.TERM_PRIM],
               (SymbolTypes.TERM_PRIM, TokenTypes.DIV): [TokenTypes.DIV, SymbolTypes.FACTOR, SymbolTypes.TERM_PRIM],

               (SymbolTypes.FACTOR, TokenTypes.MINUS): [TokenTypes.MINUS, SymbolTypes.UNSIGNED_FACTOR],
               (SymbolTypes.FACTOR, TokenTypes.LEFT_BRACKET): [SymbolTypes.UNSIGNED_FACTOR],
               (SymbolTypes.FACTOR, TokenTypes.NUMBER): [SymbolTypes.UNSIGNED_FACTOR],

               (SymbolTypes.UNSIGNED_FACTOR, TokenTypes.LEFT_BRACKET): [TokenTypes.LEFT_BRACKET, SymbolTypes.EXPRESSION,
                                                                        TokenTypes.RIGHT_BRACKET],
               (SymbolTypes.UNSIGNED_FACTOR, TokenTypes.NUMBER): [TokenTypes.NUMBER], }
