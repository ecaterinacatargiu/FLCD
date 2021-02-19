class FA:

    def __init__(self):
        self.states = []
        self.alphabet = []
        self.initialState = None
        self.finalStates = []
        self.transitions = []

        self.readFromFile()

    def readFromFile(self):
        filename = "fa.in"
        f = open(filename, "r")

        self.states = f.readline().split(" ")
        self.states[-1] = self.states[-1].strip("\n")

        self.alphabet = f.readline().split(" ")
        self.alphabet[-1] = self.alphabet[-1].strip("\n")

        self.initialState = f.readline()
        self.initialState = self.initialState.strip("\n")

        self.finalStates = (f.readline().split(" "))
        self.finalStates[-1] = self.finalStates[-1].strip("\n")

        for line in f:
            self.transitions.append(line[:-1].split(" "))

    def getStates(self):
        print("Q = { " + ", ".join(self.states) + " }")

    def getAlphabet(self):
        print("E = { " + ", ".join(self.alphabet) + " }")

    def getFinalState(self):
        print("F = { " + ", ".join(self.finalStates) + " }")

    def getInitialState(self):
        print("q0 = " + str(self.initialState))

    def getTransitions(self):
        print("S : { ")
        for el in self.transitions:
            print(el[0] + " -> " + el[1] + " : " + el[2])
        print(" }")

    def getFA(self):
        print(self.getStates())
        print(self.getAlphabet())
        print(self.getInitialState())
        print(self.getFinalState())
        print(self.getTransitions())

    def getTransFforState(self, state):
        allTransitions = []
        for tran in self.transitions:
            if tran[0] == state:
                allTransitions.append([tran[1], tran[2]])
        return allTransitions

    def checkDFA(self, sequence):
        currentState = self.initialState
        isDFA = 1
        index = 0
        while True:
            availableTrans = self.getTransFforState(currentState)
            for trans in availableTrans:
                if sequence[index] == trans[1]:
                    isDFA = 1
                    currentState = trans[0]
                    index += 1
                else:
                    isDFA = 0
            if isDFA == 0:
                return False
            elif index == len(sequence) - 1 and currentState in self.finalStates:
                return True