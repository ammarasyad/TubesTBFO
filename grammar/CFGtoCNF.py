import os


def get_cfg(filename):
    cfg = []
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith("// Terminal"):
            break
        if line.startswith("//") or line == "\n":
            continue
        line = line.replace(" -> ", " ").replace("\n", "")
        prod = line.split()
        if "|" in prod:
            temp = [prod[0]]
            for p in prod[1:]:
                if p != "|":
                    temp.append(p)
                else:
                    cfg.append(temp)
                    temp = [prod[0]]
            cfg.append(temp)
        else:
            cfg.append(prod)
    return cfg


def get_terminals(filename):
    term_rules = []
    with open(filename) as f:
        lines = f.readlines()
    start = [lines.index(i) for i in lines if i.startswith("// Terminal")][0]
    for line in lines[start:]:
        if line.startswith("//") or line == "\n":
            continue
        line = line.split(" -> ")
        line[1] = line[1].replace("\n", "")
        term_rules.append(line)
    return [i[0] for i in term_rules], term_rules


def remove_unit_productions(cfg, terminals):
    to_be_removed = []
    for prod in cfg:
        if len(prod) == 2 and prod[1] not in terminals:
            index = cfg.index(prod) + 1
            unit = prod[1]
            temp = [prod[0]]
            for p in cfg:
                if p[0] == unit:
                    temp.append(p[1:])
            for t in temp:
                if temp[0] == t:
                    continue
                to_be_inserted = [temp[0], *t]
                if to_be_inserted not in cfg:
                    cfg.insert(index, to_be_inserted)
                    index += 1
            to_be_removed.append(prod)
    for prod in to_be_removed:
        cfg.remove(prod)
    return cfg


def get_rule(terminal, rules):
    return [rule for rule in rules if rule[0] == terminal][0][0]


def check_rhs(cfg):
    idx = 1
    for prod in cfg:
        if len(prod) > 3:
            rule = []
            for i in range(2, len(prod)):
                rule.append(prod[i])
            for i in range(2, len(prod)):
                prod.pop()
            new_rule = rule[0]
            for e in cfg:
                if new_rule in e[0]:
                    new_rule += "_RULE"
                    break
            prod.append(new_rule)
            rule.insert(0, new_rule)
            if rule not in cfg:
                cfg.insert(idx, rule)
        idx += 1
    return cfg


def convert(filename):
    cfg = get_cfg(filename)
    terminals, term_rules = get_terminals(filename)
    cfg = remove_unit_productions(cfg, terminals)
    for rule in term_rules:
        cfg.append(rule)
    cfg = check_rhs(cfg)
    with open(os.getcwd() + r"\cnf.txt", "w") as f:
        for prod in cfg:
            f.write(" ".join(prod).replace(" ", " -> ", 1) + "\n")


if __name__ == "__main__":
    convert(os.getcwd() + r"\cfg.txt")
