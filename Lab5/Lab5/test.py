# input definition
# first line the initial nonTerminal
# second line the terminals with spaces between elements
# third line the nonTerminals
# next lines the productions

class Lr0Parser:
    def __init__(self, file_path):
        file_program = self.read_program(file_path)
        self.terminals = file_program[0]
        self.nonTerminals = file_program[1]
        self.productions = {}
        self.transactions = file_program[2:]
        for elements in self.transactions:
            if elements[0] in self.productions:
                self.productions[elements[0]].append(elements[1:])
            else:
                self.productions[elements[0]] = [elements[1:]]
        self.data = [self.terminals, self.nonTerminals, self.productions]
        dotted = self.dotMaker()

        self.initial_closure = {"S'": [dotted["S'"][0]]}
        self.closure(self.initial_closure, dotted, dotted["S'"][0])

    def dotMaker(self):
        self.dottedproductions = {'S\'': [['.', 'S']]}
        for nonTerminal in self.productions:
            self.dottedproductions[nonTerminal] = []
            for way in self.productions[nonTerminal]:
                self.dottedproductions[nonTerminal].append(["."] + way)

        return self.dottedproductions

    def closure(self, closure_map, transitions_map, transition_value):
        dot_index = transition_value.index(".")
        if dot_index + 1 == len(transition_value):
            return
        after_dot = transition_value[dot_index + 1]
        if after_dot in self.nonTerminals:
            non_terminal = after_dot

            if non_terminal not in closure_map:
                closure_map[non_terminal] = transitions_map[non_terminal]
            else:
                closure_map[non_terminal] += transitions_map[non_terminal]
            for transition in transitions_map[non_terminal]:
                self.closure(closure_map, transitions_map, transition)

    @staticmethod
    def shiftable(transition):
        dot_index = transition.index(".")
        if len(transition) > dot_index + 1:
            return True
        return False

    @staticmethod
    def shift_dot(transition):
        transition = transition[:]
        dot_index = transition.index(".")
        if not Lr0Parser.shiftable(transition):
            raise Exception("Should I shift it back ?")

        if len(transition) > dot_index + 2:
            remainder = transition[dot_index + 2:]
        else:
            remainder = []
        transition = transition[:dot_index] + [transition[dot_index + 1]] + ["."] + remainder
        return transition

    def canonical_collection(self):
        self.idk = {}
        self.queue = [{
            "state": self.initial_closure,
            "initial_dotted": self.dottedproductions,
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

    def goto_one(self, initial_dotted, key, state, parent=-1):
        shifted_transition = self.shift_dot(state)
        closure_map = {key: [shifted_transition]}
        self.closure(closure_map, initial_dotted, shifted_transition)
        self.queue.append({
            "state": closure_map,
            "initial_dotted": initial_dotted,
            "parent": parent,
            "parent_key": shifted_transition[shifted_transition.index(".") - 1]
        })

    def get_reduced(self):
        self.reduced = {}
        for state in self.states:
            state_key = list(state.keys())[0]
            if len(state) == 1 and len(state[state_key]) and len(state[state_key][0]) \
                    and state[state_key][0][-1] == ".":
                self.reduced[self.states.index(state)] = state
        return self.reduced

    @staticmethod
    def read_program(file_path):
        file1 = open(file_path, 'r')
        lines = file1.readlines()
        file1.close()
        return [line.replace("\n", "").replace("\t", "").split(" ") for line in lines]

    @staticmethod
    def print_dict(hashmap, message=None, deepness=""):
        if message is not None:
            print(deepness + message)
        for key in hashmap:
            print(f"{deepness}{key} : {hashmap[key]}");

    def print_data(self, index=-1):
        if index == -1:
            exit()
        else:
            print(self.data[index - 1])

    def print_production(self, non_terminal):
        data = self.data[2]
        if non_terminal in data:
            for row in data[non_terminal]:
                print(f"{non_terminal} -> {row}")
        else:
            print("Wrong non terminal!")


def show_menu():
    lr0 = Lr0Parser("g0.txt")

    print("""
    1 - print terminals
    2 - print non terminals
    3 - print productions
    4 - print productions for a given non terminal
    5 - canonical collection
    6 - exit
    """)
    menu = {
        "1": lambda: lr0.print_data(1),
        "2": lambda: lr0.print_data(2),
        "3": lambda: lr0.print_data(3),
        "4": lambda: lr0.print_production(input("Please give a non terminal:")),
        "5": lambda: lr0.canonical_collection(),
        "6": exit
    }
    while True:
        option = input("Choose an option:")
        if option in menu:
            menu[option]()
        else:
            print("Wrong option")


if __name__ == '__main__':
    show_menu()