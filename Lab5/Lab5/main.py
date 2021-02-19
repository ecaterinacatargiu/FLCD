import sys
from Grammar import Grammar

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gr = Grammar()
    gr.read_from_file(sys.argv[1])
    print(gr)
    print(gr.get_productions_for_nonterminal("simpelStmt"))
