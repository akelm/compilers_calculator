from typing import Optional


class State:
    def __init__(self, on_digit: Optional[int], on_starting_operator: Optional[int], on_operator: Optional[int],
                 on_whitespace: Optional[int], on_other: Optional[int], accepting: str):
        self._on_digit = on_digit
        self._on_starting_operator = on_starting_operator
        self._on_operator = on_operator
        self._on_whitespace = on_whitespace
        self._on_other = on_other
        self.accepting: str = accepting

    def on_digit(self) -> Optional[int]:
        return self._on_digit

    def on_starting_operator(self) -> Optional[int]:
        return self._on_starting_operator

    def on_operator(self) -> Optional[int]:
        return self._on_operator

    def on_whitespace(self) -> Optional[int]:
        return self._on_whitespace

    def on_other(self) -> Optional[int]:
        return self._on_other
