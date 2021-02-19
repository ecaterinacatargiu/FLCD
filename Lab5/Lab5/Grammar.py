from collections import defaultdict

class Grammar(object):

    def __init__(self):
        self.terminals = []
        self.non_terminals = []
        self.productions = defaultdict(list)
        self.starting_symbol = ""

    def __str__(self):
        stringu = "The grammar is:\nSet of terminals= "
        for c in self.terminals:
            stringu+=c + " "
        stringu+="\nSet of non terminals= "
        for c in self.non_terminals:
            stringu+=c + " "
        stringu+="\nThe productions:\n"
        for non_term in self.productions:
            prods = self.productions[non_term]
            stringu+= str(non_term) + "-> "
            for element in prods:
                stringu+=str(element) + " | "
            if len(prods) != 0:
                stringu = stringu[:-3]
            stringu+="\n"
        return stringu

    def get_productions_for_nonterminal(self, non_terminal):
        try:
            x = self.productions[non_terminal]
            return x
        except:
            raise Exception("No such non terminal exists")


    def read_from_file(self,path):
        with open(path, "r") as f:
            startingSymbol = f.readline().strip("\n\r")
            self.starting_symbol = startingSymbol

            line = f.readline()
            for c in line.split(" "):
                self.non_terminals.append(c)
            if self.starting_symbol not in self.non_terminals:
                raise Exception("No start symbol given! Bad grammar!")

            line = f.readline()
            for c in line.split(" "):
                self.terminals.append(c)
            lines = f.readlines()
            for line in lines:
                non_term, prods = line.split(" ", 1)
                for prod in prods.split(" "):
                    if "@" in prod:
                        prod = prod.replace("@", " ")
                    prod = prod.rstrip()
                    prod = "\"" + prod + "\""
                    self.productions[non_term].append(prod)

    def closure(self, element):
        pass


class Lr0Parser(object):
    def __init__(self, grammar):
        self.terminals = grammar.terminals
        self.non_terminals = grammar.non_terminals
        self.productions = grammar.productions
        self.starting_symbol = grammar.starting_symbol
        self.augmented_grammar = None
        self.dotted_productions = None

    def start_magic(self):
        self.augment_grammar()
        self.initial_closure = self.dotted_productions['S\'']
        self.closure(self.initial_closure, self.dotted_productions, self.dotted_productions['S\''][0])

    def augment_grammar(self):
        self.dotted_productions = defaultdict(list)

        self.dotted_productions['S\''].append(".S") #augmented start

        for non_terminal in self.productions:
            self.dotted_productions[non_terminal] = []
            for way in self.productions[non_terminal]:
                self.dotted_productions[non_terminal].append("." + way)

    def closure(self, element, closure_history, transition_history):
        dot_index = element.index('.')
        if "." == element[-1]:
            return
        element_after_dot = element[dot_index + 1 if element[dot_index+1] != " " else dot_index+2 : element.find(" ", dot_index+1)]
        if element_after_dot in self.non_terminals:
            non_terminal = element_after_dot

            if non_terminal not in closure_history:
                closure_history[non_terminal] = transition_history[non_terminal]
            else:
                closure_history[non_terminal] += transition_history[non_terminal]
            for transition in transition_history[non_terminal]:
                self.closure(transition, closure_history, transition_history)

    def shift_dot(self, transition):
        transition = transition[:]
        dot_index = transition.index(".")

        if transition[-1] == ".":
            raise Exception("No more shifting available!")

        transition_after_dot = transition[dot_index + 1 if transition[dot_index+1] != " " else dot_index+2 : ]
        transition_before_dot = transition[: dot_index]
        shifted_transition =  transition_before_dot + ". " + transition_after_dot

        return shifted_transition

    def goto_one(self, initial_dotted, key, state, parent=-1):

        shifted_transition = self.shift_dot(state)
        closure_history = {key: [shifted_transition]}

        self.closure(shifted_transition, closure_history, initial_dotted)

        self.queue.append({
            "state": closure_history,
            "initial_dotted": initial_dotted,
            "parent": parent,
            "parent_key": shifted_transition[shifted_transition.rfind(" ", shifted_transition.index(".")-2): \
                                             shifted_transition.index(".") - 1]
        })

    def goto_all(self, state, initial_dotted, parent=-1, parent_key="-1"):
        if state not in self.states:
            self.states.append(state)
            index = len(self.states) - 1
            self.state_parents[index] = {
                "parent_index": parent,
                "before_dot": parent_key
            }
            {}.items()
            self.print_dict(state, f"state {index}")
            for key in state:
                for transition in state[key]:
                    if self.shiftable(transition):
                        self.goto_one(initial_dotted, key, transition, index)
        else:
            if parent in self.idk:
                self.idk[parent][parent_key] = self.states.index(state)
            else:
                self.idk[parent] = {parent_key: self.states.index(state)}

    def canonical_collection(self):
        self.idk = {}
        self.queue = [{
            "state": self.initial_closure,
            "initial_dotted": self.dotted_productions,
        }]
        self.states = []
        self.state_parents = {}
        while len(self.queue) > 0:
            self.goto_all(**self.queue.pop(0))
        reduced = self.get_reduced()
        for k in reduced:
            red_k = list(reduced[k].keys())
            if red_k[0] != "S'":
                trans = red_k + reduced[k][red_k[0]][0][:-1]
                reduce_index = self.transactions.index(trans) + 1
                self.idk[k] = { terminal: f"r{reduce_index}" for terminal in self.terminals}
                self.idk[k]["$"] = f"r{reduce_index}"
            else:
                self.idk[k] = {"$": "accept"}
        del self.state_parents[0]
        for key in self.state_parents:
            parent = self.state_parents[key]
            if parent["parent_index"] in self.idk:
                self.idk[parent["parent_index"]][parent["before_dot"]] = key
            else:
                self.idk[parent["parent_index"]] = {parent["before_dot"]: key}
        table = {f"I{index}" : self.idk[index] for index in range(len(self.states))}
        self.print_dict(table, "Table:")
