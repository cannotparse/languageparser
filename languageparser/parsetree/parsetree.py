from typing import List


class ParseTree(object):

    def __init__(self, derivations: List[object], input_string: str):
        self.derivations = derivations
        self.input = input
