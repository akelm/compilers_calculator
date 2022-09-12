import operator
import string
from typing import List, Optional, Union, Callable

from classes import Token, SymbolTree
from settings import all_chars, TokenTypes, op_dict_str, assign_dict, SymbolTypes, parse_table, whitespace


class LexerError(Exception):
    pass


class ParserError(Exception):
    pass


class PrefixTranslationError(Exception):
    pass


def lexer(text: str) -> List[Token]:
    """
    Scans and tokenizes the arithmetic expression with number evaluation and translation of operators to functions.
    :param text: arithmetic expression
    :return: list of tokens
    """
    tokens: List[Token] = []
    digits: str = ""
    for ch in text:
        if ch not in all_chars:
            raise LexerError("Character:", ch, "outside the allowed characters.")
        if ch in string.digits:
            digits += ch
        else:
            if digits:
                tokens.append(Token(TokenTypes.NUMBER, int(digits)))
                digits = ""
            if ch not in whitespace:
                value: Optional[callable] = op_dict_str[ch] if ch in op_dict_str.keys() else None
                token_type: TokenTypes = assign_dict[ch]
                tokens.append(Token(token_type, value))
    if digits:
        tokens.append(Token(TokenTypes.NUMBER, int(digits)))
    tokens.append(Token(TokenTypes.END, None))
    return tokens


def parser(token_list) -> SymbolTree:
    """
    Builds the symbol tree from tokens according to the grammar.
    :param token_list: tokenized string
    :return: the head of the symbol tree
    """
    if not token_list:
        raise ParserError("Empty token list!")
    if len(token_list) == 1:
        if token_list[0] == TokenTypes.END:
            raise ParserError("Token list contains only TokenTypes.END!")
    head: SymbolTree = SymbolTree(SymbolTypes.EXPRESSION) if token_list else None
    symbol_stack: List[SymbolTree] = [head] if head else []
    for token in token_list:
        if not symbol_stack:
            raise ParserError("Symbol stack is empty!")
        while symbol_stack and not isinstance(symbol_stack[0].sym_type, TokenTypes):
            if (symbol_stack[0].sym_type, token.type) not in parse_table:
                raise ParserError("The key:", symbol_stack[0].sym_type, token.type, "not present in the parse table!")
            symbol: SymbolTree = symbol_stack.pop(0)
            new_symbols: List[Union[TokenTypes, SymbolTypes]] = parse_table[(symbol.sym_type, token.type)]
            if SymbolTypes.EMPTY not in new_symbols:
                for s in new_symbols[::-1]:
                    expr = SymbolTree(s)
                    symbol_stack.insert(0, expr)
                    symbol.children.insert(0, expr)
        if symbol_stack:
            if symbol_stack[0].sym_type != token.type:
                raise ParserError("The token of type:", token.type, "does not match the symbol expected from stack:",
                                  symbol_stack[0].sym_type, "!")
            symbol: SymbolTree = symbol_stack.pop(0)
            symbol.value = token.value
            if symbol.value == operator.sub \
                    and symbol_stack \
                    and symbol_stack[0].sym_type == SymbolTypes.UNSIGNED_FACTOR:
                symbol.sym_type = TokenTypes.UNARY_MINUS
                symbol.value = operator.neg
    if symbol_stack:
        raise ParserError("Unexpected end of tokens while stack non-empty!")
    return head


def to_prefix(expression: List[Union[List, callable, int]]) -> List[Union[List, callable, int]]:
    """
    Translates the expression of the form: [<operand1>, [binary operator, operand2]] OR [unary_operator, operand2]
    to prefix notation.
    :param expression: nested list of operator callables and ints produces by SymbolTree.reduce()
    :return: list of the form: [binary operator, operand1, operand2] or [unary_operator, operand2]
    """
    if not isinstance(expression, list):
        return expression
    if len(expression) == 3 and isinstance(expression[0], Callable):
        return expression
    if len(expression) != 2:
        raise PrefixTranslationError("The list:", expression, "should contain 2 elements!")
    if not callable(expression[0]):
        lhs = to_prefix(expression[0])
        children = expression[1]
        op = children[0]
        rhs = to_prefix(children[1])
        if len(children) > 3:
            prefix_expression = to_prefix([[op, lhs, rhs], children[2:]])
        elif len(children) == 3:
            # children = children[0]
            prefix_expression = to_prefix([[op, lhs, rhs], children[2]])
        else:
            prefix_expression = [op, lhs, rhs]  # prefix_expression[0:2]=prefix_expression[1::-1]
    else:  # unary minus
        prefix_expression = expression
        prefix_expression[1:] = list(map(to_prefix, prefix_expression[1:]))
    return prefix_expression


def evaluate(prefix_expression: List[Union[List, callable, int]]) -> int:
    """
    Evaluates the expression in the prefix notation
    :param prefix_expression:
    :return: result: int
    """
    if not isinstance(prefix_expression, list):
        return prefix_expression
    else:
        operands = list(map(evaluate, prefix_expression[1:]))
        return prefix_expression[0](*operands)


def calculate(text: str) -> int:
    tokens = lexer(text)
    h = parser(tokens)
    h_eval = h.reduce()
    pref_not = to_prefix(h_eval)
    result = evaluate(pref_not)
    return result


def calculate_nan(text: str) -> Optional[int]:
    try:
        return calculate(text)
    except Exception:
        return
