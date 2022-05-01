from collections import defaultdict
from typing import List, DefaultDict, Callable

from settings import State, states, digits,starting_operators ,operators, whitespaces,operations , operator_assignment , digit_collecting



class Automaton:
    def __init__(self):
        if not states:
            raise ValueError("states_list cannot be empty!")
        self._states_list : List[State] = states
        self._state_number: int = 0
        if not (digits and starting_operators and operators and whitespaces):
            raise ValueError("Neither of digits, operators and whitespaces can be empty!")
        self._on_input: DefaultDict[str, Callable] = defaultdict(lambda: State.on_other)
        for d in digits:
            self._on_input[d] = State.on_digit
        for o in starting_operators:
            self._on_input[o] = State.on_starting_operator
        for o in operators:
            self._on_input[o] = State.on_operator
        for w in whitespaces:
            self._on_input[w] = State.on_whitespace
        self._value: float = .0
        self._number: str = ''
        self._operator: Callable = operations['']


    def new_state(self, x: str) -> bool:
        current_state: State = self._states_list[self._state_number]
        next_state_num = self._on_input[x](current_state)
        if next_state_num is None:
            return False
        else:
            if (self._state_number,next_state_num) in digit_collecting:
                self._number+=x
            if (self._state_number,next_state_num) in operator_assignment:
                self._value = self._operator(self._value, int(self._number))
                self._number = ''
                self._operator = operations[x]
            self._state_number = next_state_num
            return True

    def check_accepting(self) -> str:
        return self._states_list[self._state_number].accepting

    def get_final_result(self) -> float:
        if self._number:
            self._value = self._operator(self._value, int(self._number))
            self._number = ''
        return self._value


