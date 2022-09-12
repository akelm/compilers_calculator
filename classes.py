from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union, List

from settings import TokenTypes, SymbolTypes


@dataclass
class Token:
    type: TokenTypes
    value: Union[callable, int]


@dataclass
class SymbolTree:
    children: List[SymbolTree] = field(init=False, default_factory=list)
    sym_type: Union[SymbolTypes, TokenTypes] = field(init=True, default=None)
    value: Union[str, int, callable] = field(init=False, default=None)

    def reduce(self):
        if isinstance(self.sym_type, TokenTypes):
            return self.value
        else:
            child_eval = list(filter(lambda x: x is not None, map(SymbolTree.reduce, self.children)))
            if not child_eval:
                return
            elif len(child_eval) == 1:
                return child_eval[0]
            else:
                return child_eval
