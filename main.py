from symbol_table import SymbolTable
from parser import Parser
from program import Code
import sys

def main():
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        code = f.read()

    ast = Parser.run(code)
    st = SymbolTable()
    ast.evaluate(st)
    ast.generate(st)
    Code.dump()

main()