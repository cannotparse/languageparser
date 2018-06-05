from typing import Dict, List
import re
import pdb


"""
Assumption: Whitespace is ignored by this grammar
Assumption: symbols are separated by a space
"""


class Symbol(object):

    def __eq__(self, other):
        return self.name == other.name

    @classmethod
    def _is_named(cls, string):
        match = re.match(r'<([A-Za-z-]{1,})>', string)
        if match:
            return True
        return False


class NonTerminal(Symbol):

    def __init__(self, name, productions: List[List[Symbol]]):
        self.name = name
        self._productions = productions
        self.size = len(productions)



class Terminal(Symbol):
    """
    Represents a single character to be used as a terminal.
    """

    def __init__(self, name, character: str):
        self.name = name
        self.character = character


class NullTerminal(Symbol):
    size = 0


class Cfg(object):
    """
    Represents a context free grammar with productions.
    """

    def __init__(self, grammar: List[str]):
        """
        Creates a grammar from a provided set of strings that represent
        productions of the grammar
        """
        self._productions = Cfg._parse_grammar(grammar=grammar)

    @classmethod
    def _parse_grammar(cls, grammar: List[str]) -> Dict[str, List[Symbol]]:
        """
        Converts string a list of productions to a dict of productions for use
        by a CFG.
        """
        re_production = r'(.*)->(.*)'
        pre_productions = {}
        productions = {}
        # Will get all Terminals will be linked. Nonterms are still strings
        for string_prod in grammar:
            match = re.match(re_production, string_prod)
            # pdb.set_trace()
            if match:
                pre_productions[match.group(1).strip()] = \
                    cls._parse_production(match.group(2))
        for prod in pre_productions.keys():
            productions[prod] = NonTerminal(prod, pre_productions[prod])

        # Find symbols for productions inside other productions
        for prod in productions.keys():
            # Productions have multiple derivations
            for derivation in productions[prod]._productions:
                # For each symbol in this derivaton
                for i in range(len(derivation)):
                    # find if this represents a NonTerminal symbol (production)
                    if type(derivation[i]) is str:
                        if derivation[i] in productions:
                            derivation[i] = productions[prod]
                        else:
                            raise ValueError("Cannot find corresponding symbol for {}".format(derivation[i]))
        return productions

    @classmethod
    def _parse_production(cls, production: str):
        """
        Converts string production to deserialized objects of all productions
        """
        productions = []
        string_productions = production.split('|')
        for string_production in string_productions:
            productions.append(cls._parse_symbols(string_production.strip()))
        return productions

    @classmethod
    def _parse_symbols(cls, production: str):
        str_symbols = production.split(' ')
        # Seperate Terminals from named NonTerminals
        symbols = []
        for symbol in str_symbols:
            if Symbol._is_named(symbol):
                symbols.append(symbol)
            else:
                symbols.append(Terminal(symbol, symbol))
        return symbols


if __name__ == '__main__':
    d = """<E> -> a <B>
    <B> -> <A> | e <E> <A> t
    <A> -> a | b | c | d | e
    """
    t = d.split('\n')
    h = Cfg(t)
    print(h._productions)
    pdb.set_trace()
