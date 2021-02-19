from collections import defaultdict
from copy import deepcopy
from collections import deque

class Grammar(object):

    def __init__(self):
        self.terminals = []
        self.non_terminals = []
        self.productions = defaultdict(list)
        self.starting_symbol = ""

    def __str__(self):
        stringu = "The grammar is:\nSet of terminals = "
        for c in self.terminals:
            stringu += c + " "
        stringu += "\nSet of non terminals = "
        for c in self.non_terminals:
            stringu += c + " "
        stringu += "\nThe productions: \n"
        for non_term in self.productions:
            prods = self.productions[non_term]
            stringu += str(non_term) + " -> "
            for element in prods:
                stringu += str(element) + " | "
            if len(prods) != 0:
                stringu = stringu[:-3]
            stringu += "\n"
        return stringu

    def get_productions_for_nonterminal(self, non_terminal):
        try:
            x = self.productions[non_terminal]
            return x
        except:
            raise Exception("No such non terminal exists")

    def read_from_file(self, path):
        with open(path, "r") as f:
            startingSymbol = f.readline().strip("\n\r")
            self.starting_symbol = startingSymbol

            line = f.readline()
            for c in line.split(" "):
                self.non_terminals.append(c.strip("\n\r"))
            if self.starting_symbol not in self.non_terminals:
                raise Exception("No start symbol given! Bad grammar!")

            line = f.readline()
            for c in line.split(" "):
                self.terminals.append(c.strip("\n\r"))
            lines = f.readlines()
            for line in lines:
                non_term, prods = line.split(" ", 1)
                for prod in prods.split(" "):
                    if "@" in prod:
                        prod = prod.replace("@", " ")
                    prod = prod.rstrip()
                    prod = "\"" + prod + "\""
                    self.productions[non_term].append(prod)