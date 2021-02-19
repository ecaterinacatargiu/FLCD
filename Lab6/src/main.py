import sys
from Grammar import Grammar
from Parser import Lr0Parser

if __name__ == '__main__':
    gr = Grammar()
    gr.read_from_file("D:\An III\FLCD\Lab\Lab6\src\g1.txt")
    print(gr)
    parser = Lr0Parser(gr)
    parser.canonical_collection()
    parser.actual_parsing(['b', 'a', 'a', 'b'])
