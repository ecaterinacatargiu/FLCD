from FA.FiniteAutomaton import FA

def printSubmenu():
    print("What do you want to do ? ")
    print("1. Read the FA from file")
    print("2. See set fo states: Q")
    print("3. See the alphabet: E")
    print("4. See the final states: F")
    print("5. See the inital state")
    print("6. See the transitions")
    print("7. Check DFA")

def main():

    print("Choose how you want to get the finite automaton elements: ")
    print("1. Read from file")
    while(True):
        command = int(input("Enter your option: "))
        if command == 1:
            print("You chose to read from file")
            fa = FA()
            printSubmenu()
            while(True):
                cmd = int(input("Enter what you want to see: "))
                if cmd == 1:
                    print(fa.getFA())
                elif cmd == 2:
                    print(fa.getStates())
                elif cmd == 3:
                    print(fa.getAlphabet())
                elif cmd == 4:
                    print(fa.getFinalState())
                elif cmd == 5:
                    print(fa.getInitialState())
                elif cmd == 6:
                    print(fa.getTransitions())
                elif cmd == 7:
                    sequence = input("Input the sequence: ")
                    print(fa.checkDFA(sequence))
                elif cmd == 0:
                    break
                else:
                    print("Try a valid option ;)")

main()