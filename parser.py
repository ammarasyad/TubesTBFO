import os

from time import perf_counter
from grammar.automata import check_name, check_arithmetic
from grammar.CFGtoCNF import convert
# from grammar.cyk import Parser
from grammar.cyk import cyk_algorithm


def _check_value_grammar(grammar, value):
    for values in grammar.values():
        for v in values:
            if v == value:
                return True
    return False


def _check_num_var(processed, grammar):
    for i, v in enumerate(processed):
        if not _check_value_grammar(grammar, v):
            try:
                float(v)
                processed[i] = "num"
            except ValueError:
                if check_name(v):
                    processed[i] = "word"
    return processed


def _parse_comments(processed):
    for i, v in enumerate(processed):
        if v == "/*":
            j = i
            while processed[j] != "*/":
                j += 1
            del processed[i:j + 2]
    return processed


def _parse_fa(processed):
    for i, v in enumerate(processed):
        if check_arithmetic(v):
            processed[i] = "arithmetic"
        elif check_name(v):
            processed[i] = "word"
        else:
            try:
                float(v)
                processed[i] = "num"
            except ValueError:
                pass
    return processed


def parse_cnf(cnf_file):
    grammar = {}
    with open(cnf_file) as f:
        lines = f.readlines()
    for line in lines:
        line = line.split("->")
        if line[0].strip() in grammar.keys():
            grammar[line[0].strip()] += [line[1].replace("\n", "").strip()]
        else:
            grammar[line[0].strip()] = [line[1].replace("\n", "").strip()]
    return grammar


def parse(filename: str):
    cfg = os.getcwd() + r"\grammar\cfg.txt"
    cnf = os.getcwd() + r"\grammar\cnf.txt"
    start = perf_counter()
    convert(cfg)
    cnf_parsed = parse_cnf(cnf)
    try:
        with open(filename) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("File not found. Please enter a valid filename.")
        exit(1)
    except NotADirectoryError:
        print("The file inputted is a directory.")
        exit(2)
    if not lines:
        print("Accepted")
        exit(0)

    symbols = ['{', '}', '(', ')', '+', '-', '*', '/', '%', '!', '>', '<', ';',
               '&&', '||', '=', '\n', '?', '"', "'", '[', ']', ':', ',']
    symbol2 = ['=  =  =', '!  =  =', '=  =', '!  =', '>  =', '<  =', '*  *', '>  >  >', '<  <',
               '>  >', '&  &', '|  |', '+  +', '-  -', '/  /', '*  /', '/  *']

    processed = []
    for line in lines:
        if line.startswith("//"):
            continue
        for symbol in symbols:
            if line.startswith("/*") or line.startswith("*") or line.startswith("*/"):
                continue
            line = line.replace(symbol, " " + symbol + " ")
        for symbol in symbol2:
            line = line.replace(symbol, symbol.replace(' ', ''))
        line = line.split(" ")
        line = [x for x in line if x != ""]
        processed.extend(line)
    processed = _parse_comments(processed)
    processed = _check_num_var(processed, cnf_parsed)

    cyk_algorithm(cnf_parsed, processed)
    # x = []
    # for c in processed:
    #     if c == "\n":
    #         x += [["newline"]]
    #     cyk = Parser(cnf, c)
    #     x += cyk.parse()
    # for i, k in enumerate(x):
    #     p = k[0]
    #     for j in x[i + 1:]:
    #         if j == ["newline"]:
    #             break
    #         try:
    #             p.append(j[0])
    #         except Exception:
    #             continue
    #     if p == "newline":
    #         continue
    # print("Accepted")
    print(f"File parsed in {perf_counter() - start} seconds.")
