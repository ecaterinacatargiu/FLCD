from collections import defaultdict, deque
from copy import deepcopy

class Lr0Parser(object):
    def __init__(self, grammar):
        self.grammar = grammar
        self.terminals = grammar.terminals
        self.non_terminals = grammar.non_terminals
        self.productions = grammar.productions
        self.starting_symbol = grammar.starting_symbol
        self.augmented_grammar = None
        self.dotted_productions = None
        self.user_friendly_productions()
        self.start_magic()

    def start_magic(self):
        self.augment_grammar()
        self.initial_closure = {"S\'": self.dotted_productions['S\'']}
        self.closure(self.dotted_productions['S\''][0], self.initial_closure, self.dotted_productions)

    def augment_grammar(self):
        self.dotted_productions = defaultdict(list)

        self.dotted_productions['S\''].append(". " + self.grammar.starting_symbol)  # augmented start

        for non_terminal in self.productions:
            self.dotted_productions[non_terminal] = []
            for production in self.productions[non_terminal]:
                self.dotted_productions[non_terminal] \
                    .append(". "
                            + production.replace('\"', ""))  # eliminating double quotations

    def user_friendly_productions(self):
        self.uf_productions = []
        for x in self.productions:
            for productions in self.productions[x]:
                self.uf_productions.append([x] + [lmbd.strip("\"") for lmbd in productions.split(" ")])

    def closure(self, element, closure_history, transition_history):
        dot_index = element.index('.')
        if "." == element[-1]:
            return

        next_space = element.find(" ", dot_index + 2)
        if next_space == -1:
            element_after_dot = element[dot_index + 2:]
        else:
            element_after_dot = element[dot_index + 2: next_space]

        if element_after_dot in self.non_terminals:
            non_terminal = element_after_dot

            if non_terminal not in closure_history:
                closure_history[non_terminal] = transition_history[non_terminal]
            else:
                closure_history[non_terminal] += transition_history[non_terminal]
            for transition in transition_history[non_terminal]:
                self.closure(transition, closure_history, transition_history)

    def shift_dot(self, transition_ref):
        transition = deepcopy(transition_ref)
        dot_index = transition.index(".")

        if transition[-1] == ".":
            raise Exception("No more shifting available!")

        transition_after_dot = transition[dot_index + 1 if transition[dot_index + 1] != " " else dot_index + 2:]
        transition_before_dot = transition[: dot_index]

        find_space_after_dot = transition_after_dot.find(" ")
        if -1 != find_space_after_dot:
            first_element_after_dot = transition_after_dot[:find_space_after_dot]
            rest_after_dot = transition_after_dot[find_space_after_dot + 1:]
        else:
            first_element_after_dot = transition_after_dot
            rest_after_dot = ""

        shifted_transition = transition_before_dot + " " + first_element_after_dot + " . " + rest_after_dot

        return shifted_transition.strip(" \n\r")

    def goto(self, initial_transition, key, state, parent=-1):

        shifted_transition = self.shift_dot(state)
        closure_history = {key: [shifted_transition]}

        self.closure(shifted_transition, closure_history, initial_transition)

        dot_index = shifted_transition.index(".")
        space_before_dot = shifted_transition.rfind(" ", 0, dot_index - 1)
        if -1 != space_before_dot:
            element_before_dot = shifted_transition[space_before_dot + 1:dot_index - 1]
        else:
            element_before_dot = shifted_transition[:dot_index - 1]
        parent_key = element_before_dot

        self.queue.append({
            "state": closure_history,
            "initial_dotted": initial_transition,
            "parent": parent,
            "parent_key": parent_key
        })

    def goto_all(self, state, initial_dotted, parent=-1, parent_key="-1"):
        if state not in self.states:
            self.states.append(state)
            index = len(self.states) - 1
            self.state_parents[index] = {
                "parent_index": parent,
                "before_dot": parent_key
            }
            self.pretty_print(state, "state {}".format(index))
            for key in state:
                for transition in state[key]:
                    if transition[-1] != '.':
                        self.goto(initial_dotted, key, transition, index)
        else:
            if parent in self.inner_table_values:
                if parent_key in self.non_terminals:
                    self.inner_table_values[parent][parent_key] = "{}".format(self.states.index(state))
                else:
                    self.inner_table_values[parent][parent_key] = "s{}".format(self.states.index(state))
            else:
                if parent_key in self.non_terminals:
                    self.inner_table_values[parent] = {parent_key: "{}".format(self.states.index(state))}
                else:
                    self.inner_table_values[parent] = {parent_key: "s{}".format(self.states.index(state))}

    def get_reduced(self):
        self.reduced = {}
        for state in self.states:
            state_key = list(state.keys())[0]
            if len(state) == 1 and len(state[state_key]) and len(state[state_key][0]) \
                    and state[state_key][0][-1] == ".":
                self.reduced[self.states.index(state)] = state
        return self.reduced

    def canonical_collection(self):
        self.inner_table_values = {}
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
                trans = red_k + [lmbd for lmbd in reduced[k][red_k[0]][0][:-1].split(" ")]
                transClean = []
                for x in trans:
                    if x != '':
                        transClean.append(x)

                reduce_index = self.uf_productions.index(transClean) + 1
                self.inner_table_values[k] = {terminal: "r{}".format(reduce_index) for terminal in self.terminals}
                self.inner_table_values[k]["$"] = "r{}".format(reduce_index)
            else:
                self.inner_table_values[k] = {"$": "accept"}
        del self.state_parents[0]
        for key in self.state_parents:
            parent = self.state_parents[key]
            if parent["parent_index"] in self.inner_table_values:
                if parent["before_dot"] in self.non_terminals:
                    self.inner_table_values[parent["parent_index"]][parent["before_dot"]] = "{}".format(key)
                else:
                    self.inner_table_values[parent["parent_index"]][parent["before_dot"]] = "s{}".format(key)
            else:
                if parent["before_dot"] in self.non_terminals:
                    self.inner_table_values[parent["parent_index"]] = {parent["before_dot"]: "{}".format(key)}
                else:
                    self.inner_table_values[parent["parent_index"]] = {parent["before_dot"]: "s{}".format(key)}
        table = {"I{}".format(index): self.inner_table_values[index] for index in range(len(self.states))}
        self.pretty_print(table, "Table:")

    def actual_parsing(self, word):

        if type(word) != list:
            raise Exception("Input sequence must be in list format")

        stack_alpha = deque()  # state stack
        stack_beta = deque()  # word stack
        stack_phi = deque()  # actions stack
        end = False

        class alpha_item(object):
            def __init__(self, value, number):
                self.value = value
                self.number = number

            def is_dummy(self):
                return self.value == -1

        stack_beta.append("$")
        for letter in reversed(word):
            stack_beta.append(letter)

        stack_alpha.append(alpha_item(0, -1))

        while end != True:
            current_step = stack_beta[-1]
            current_state = stack_alpha[-1]

            if "s" in self.inner_table_values[current_state.value][current_step]:
                current_step = stack_beta.pop()
                corresponding_state = int(self.inner_table_values[current_state.value][current_step][1:])
                stack_alpha.append(alpha_item(int(corresponding_state), current_step))
                stack_phi.append("Shift {}".format(corresponding_state))

            elif "r" in self.inner_table_values[current_state.value][current_step]:
                corresponding_production_index = int(self.inner_table_values[current_state.value][current_step][1:]) - 1
                lhs = self.uf_productions[corresponding_production_index][0]
                rhs = self.uf_productions[corresponding_production_index][1:]
                for value in rhs:
                    top_of_stack = stack_alpha.pop().number
                    if top_of_stack not in rhs:
                        raise Exception("Reduce failed")
                    rhs = rhs[rhs.index(top_of_stack) + 1:] + rhs[:rhs.index(top_of_stack)]

                top_alpha = stack_alpha[-1]
                stack_alpha.append(alpha_item(int(self.inner_table_values[top_alpha.value][lhs]), lhs))

                stack_phi.append("Reduced by {}".format(self.uf_productions[corresponding_production_index]))

            else:
                if 'accept' in self.inner_table_values[current_state.value][current_step]:
                    print("Success")
                else:
                    print("Nemnem")
                end = True

    def pretty_print(self, map, message=None, deepness=""):
        if message is not None:
            print(deepness + message)
        for key in map:
            print(f"{deepness}{key} : {map[key]}")
