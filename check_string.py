from typing import Union

from automaton import Automaton


def check_string(text_: str) -> str:
    if len(text_) == 0:
        return 'N'
    automaton = Automaton()
    if all(map(automaton.new_state, text_)):
        return automaton.check_accepting()
    else:
        return 'N'


def calculate_value(text_: str) -> Union[float, str]:
    if len(text_) == 0:
        return 'error'
    automaton = Automaton()
    if all(map(automaton.new_state, text_)):
        if automaton.check_accepting() == 'A':
            return automaton.get_final_result()
    return 'error'


if __name__ == "__main__":
    print("enter text:", end=" ")
    text = input()
    print("wynik: ", calculate_value(text))
