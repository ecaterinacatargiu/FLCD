import sys
from Grammar import Grammar, Lr0Parser

if __name__ == '__main__':
    gr = Grammar()
    #gr.read_from_file(sys.argv[1])
    gr.read_from_file("C:\\Users\\Breje\\Desktop\\g1.txt")
    print(gr)
    #print(gr.get_productions_for_nonterminal("simpelStmt"))
    parser = Lr0Parser(gr)
    parser.canonical_collection()
    parser.actual_parsing(['b','a','a','b'])

