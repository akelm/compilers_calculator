from typing import Union

from functions import calculate, ParserError, LexerError


def calculate_value(text_: str) -> Union[int, str]:
    try:
        return calculate(text_)
    except (ParserError, LexerError) as e:
        exc_type = type(e).__name__
        return ": ".join([exc_type, str(e)])


if __name__ == "__main__":
    print("enter an expression:", end=" ")
    text = input()
    print("wynik: ", calculate_value(text))
