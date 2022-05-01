from operator import mul, truediv, add, sub

from state import State

# states for calculator
states = [State(2, 1, None, 0, None, 'N'),
          State(2, None, None, 1, None, 'N'),
          State(2, 1, 1, 3, None, 'A'),
          State(None, 1, 1, 3, None, 'A')]

digit_collecting = [
    (0, 1),
    (0, 2),
    (1, 2),
    (2, 2)
]

operator_assignment = [
    (2, 1),
    (3, 1)
]

operations = {
    '*': mul,
    "/": truediv,
    "+": add,
    '-': sub,
    '': lambda x, y: y
}

digits = '0123456789'
starting_operators = '-'
operators = '+/*'
whitespaces = ' \t'


