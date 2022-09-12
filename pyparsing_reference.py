from parser import ParserError

import pyparsing as pp
import operator as op

ppc = pp.pyparsing_common


num = ppc.integer


op_dict = {
    "+": op.add,
    "-": op.sub,
    "*": op.mul,
    "/": op.floordiv
}

sign_op = pp.oneOf("-").addParseAction(lambda x: op.neg)
mult_op = pp.oneOf("* /").addParseAction(lambda x: op_dict[x[0]])
plus_op = pp.oneOf("+ -").addParseAction(lambda x: op_dict[x[0]])


def apply_unary(x):
    x = x[0]
    return x[0](x[1])


def apply_op(x):
    x = x[0]
    while len(x) > 1:
        op1 = x.pop(0)
        fun = x.pop(0)
        op2 = x.pop(0)
        res = fun(op1, op2)
        x.insert(0, res)
    return x[0]


expr = pp.infixNotation(
    num,
    [
        (sign_op, 1, pp.opAssoc.RIGHT, apply_unary),
        (mult_op, 2, pp.opAssoc.LEFT, apply_op),
        (plus_op, 2, pp.opAssoc.LEFT, apply_op),
    ],
)

# correct grammar
e = pp.Forward()
t_prim = pp.Forward()
e_prim = pp.Forward()

g = num | "(" + e + ")"
f = g | "-"+g
t_prim <<= "*"+f+t_prim | "/" + f + t_prim | pp.empty
t = f + t_prim
e_prim <<= "+" + t + e_prim | "-" + t + e_prim | pp.empty
e <<= t + e_prim


def parse_expr(text):
    e.parse_string(text, parse_all=True)
    res = expr.parse_string(text)
    if len(res) == 1:
        return res[0]
    else:
        raise ParserError("Result should have 1 value!")
