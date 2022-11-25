def cyk_algorithm(grammar, tokenized_input, stat=False):

    # Inisialisasi CYK Table
    cyk_table = [[[] for _ in range(i)] for i in range(len(tokenized_input), 0, -1)]

    # Array untuk Line Error checker
    check_table = [False for _ in range(len(tokenized_input))]
    pos_table = [[set() for _ in range(i)] for i in range(len(tokenized_input), 0, -1)]
    pos_table[0] = [{i} for i in range(len(tokenized_input))]

    # Inisialisasi baris pertama
    for i, token in enumerate(tokenized_input):
        for rule in grammar:
            if rule[1] == token and rule[0] not in cyk_table[0][i]:
                cyk_table[0][i].append(rule[0])
    
    # Statistik untuk debugging
    if stat:
        print()
        print(cyk_table[0])
        print(len(cyk_table[0]))
        print(len(tokenized_input))

    # Mengisi sisa table
    for i in range(1, len(cyk_table)):
        for j in range(len(cyk_table[i])):
            for k in range(i):
                left_cell = cyk_table[k][j]
                right_cell = cyk_table[i-k-1][k+j+1]

                for left in left_cell:
                    for right in right_cell:
                        targets = [left, right]

                        # Untuk line checker
                        not_deriv = True
                        for target in targets:
                            if 'deriv' in target:
                                not_deriv = False

                        for rule in grammar:
                            if rule[1:3] == targets and rule[0] not in cyk_table[i][j]:
                                cyk_table[i][j].append(rule[0])

                                pos_table[i][j] = pos_table[i][j].union(pos_table[k][j])
                                pos_table[i][j] = pos_table[i][j].union(pos_table[i-k-1][k+j+1])

                                if 'deriv' not in rule and not_deriv:
                                    for pos in pos_table[i][j]:
                                        check_table[pos] = True
    
    # Check if accepted
    if stat:
        print(check_table)
        print(len(check_table))
        print("---------Final-----------")
        for table in cyk_table:
            print(table)
            print("==========================================")
    for item in cyk_table[-1][0]:
        if item == "MAIN_STATES":
            print("Accepted")
            is_accepted = True
            break
    else:
        print("Syntax Error")
        is_accepted = False

    return check_table, is_accepted


def line_error_checker(check_table, tokenized_lines, is_accepted):
    if not is_accepted:
        error_lines = []
        for i, isCorrect in enumerate(check_table):
            if not isCorrect and tokenized_lines[i] not in error_lines:
                error_lines.append(tokenized_lines[i])

        print("Possible Error Lines : ", *error_lines)
