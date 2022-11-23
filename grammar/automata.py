import string
from tokenizer import tokenize_arithmetic


class DFAStateException(Exception):
    pass


def check_states(states: set, transitions: dict, final_state: set):
    # Check if transition states and final states are in states
    no_states = []
    for fstate in final_state:
        if fstate not in states:
            no_states.append(fstate)
    if no_states:
        raise DFAStateException(
            f"Final {'states' if len(no_states) > 1 else 'state'} {', '.join(no_states)} {'are' if len(no_states) > 1 else 'is'} not in states")
    no_states.clear()
    for key, value in transitions.items():
        if key[0] not in states:
            no_states.append(key[0])
        if value not in states:
            no_states.append(value)
    if no_states:
        raise DFAStateException(
            f"Transition {'states' if len(no_states) > 1 else 'state'} {', '.join(no_states)} {'are' if len(no_states) > 1 else 'is'} not in states")


class DFA:
    def __init__(self, states: set, alphabet: list, transitions: dict, start_state: str, final_state: set, debug=False):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_state = final_state
        self.debug = debug

    def process(self, input_str: str) -> bool:
        check_states(self.states, self.transitions, self.final_state)

        # Actually checking the input string
        current_state = self.start_state
        for c in input_str:
            if c not in self.alphabet:
                return False
            try:
                current_state = self.transitions[(current_state, c)]
            except KeyError:
                if self.debug:
                    print(f"Transition from {current_state} with {c} is not defined")
                return False
        return current_state in self.final_state


def get_dupe_indices(x, seq):
    return [i for (y, i) in zip(seq, range(len(seq))) if x == y]


def check_name(input_str: str):
    # Check if input_str is not a reserved name in JavaScript
    with open("reservedKeywords.txt") as f:
        reserved = f.read().splitlines()
    if input_str in reserved:
        return False

    # DFA Initialization
    states = {"q0", "q1"}
    alphabet = list(string.ascii_letters) + list(string.digits) + ["_"]
    # transitions = {
    #     ("q0", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"): "q1",
    #     ("q1", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"): "q1"
    # }
    transitions = {**{("q0", p): "q1" for p in string.ascii_letters + "_" + "$"},
                   **{("q1", p): "q1" for p in string.ascii_letters + string.digits + "_" + "$"}}
    start_state = "q0"
    final_states = {"q1"}

    dfa = DFA(states, alphabet, transitions, start_state, final_states)

    return dfa.process(input_str)


# TODO: Rewrite this function
def check_arithmetic(input_str: str) -> bool:
    operators = ["+", "++", "-", "--", "*", "/", "%", "&", "|", "^", "~", "<<", ">>", ">>>"]
    tokens = tokenize_arithmetic(input_str)
    variables = [v for t, v in tokens if t == "VAR"]
    ops = [v for t, v in tokens if t == "OP"]
    nums = [v for t, v in tokens if t == "NUM"]
    floats = [v for t, v in tokens if t == "FLOAT"]

    # The great filter
    # final = ["" for _ in range(len(tokens))]
    for var in variables:
        if not check_name(var):
            return False
        # final.insert(tokens.index(("VAR", var)), "v")
    for op in ops:
        if op not in operators:
            return False
        # for i in get_dupe_indices(("OP", op), tokens):
        #     final.insert(i, op)
    # for num in nums:
    #     final.insert(tokens.index(("NUM", num)), "n")
    # for flt in floats:
    #     final.insert(tokens.index(("FLOAT", flt)), "f")
    # final = " ".join([f for f in final if f != ""])
    # print(final)
    return True
    # input_str = input_str.replace(" ", "")

    # # secondary_ops = ["=", "+=", "-=", "*=", "/=", "%=", "==", "!=", ">", "<", ">=", "<=", "===", "!==", ";"]
    # filtered = [c for c in input_str.split() if c not in operators]
    # for f in filtered:
    #     if not f.isdigit():
    #         print(check_name(f))
    # states = {"q0", "q1", "q1_1", "q1_2", "q2", "q3", "q4", "q5"}
    # alphabet = list(string.ascii_letters) + list(string.digits) + operators + ["_", " "]
    # transitions = {**{("q0", p): "q1" for p in string.ascii_letters + string.digits},
    #                **{("q1", p): "q1" for p in string.ascii_letters},
    #                # check for floating point
    #                **{("q1", p): "q1_1" for p in string.digits},
    #                **{("q1_1", p): "q1_1" for p in string.digits},
    #                **{("q1_1", "."): "q1_2"},
    #                **{("q1_2", p): "q1_2" for p in string.digits},
    #                **{("q1_2", " "): "q2"},
    #                # end checking float
    #                **{("q1", " "): "q2"},
    #                **{("q2", p): "q3" for p in operators},
    #                **{("q3", p)}}
    # # transitions = {**{("q0", p): "q1" for p in string.ascii_letters + string.digits},
    # #                **{("q1", p): "q1" for p in string.ascii_letters + string.digits},
    # #                **{("q1", p): "q2" for p in operators},
    # #                **{("q2", p): "q2" for p in string.ascii_letters + string.digits + " "},
    # #                **{("q2", p): "q3" for p in string.ascii_letters + string.digits + ''.join(operators)},
    # #                **{("q2", p): "q4" for p in secondary_ops},
    # #                **{("q3", p): "q2" for p in string.ascii_letters + string.digits + " "},
    # #                **{("q3", p): "q4" for p in secondary_ops},
    # #                **{("q4", p): "q5" for p in alphabet}}
    #
    # start_state = "q0"
    # final_states = {"q3", "q4", "q5"}
    #
    # fa = DFA(states, alphabet, transitions, start_state, final_states)
    #
    # return fa.process(input_str)


if __name__ == "__main__":
    print(check_arithmetic("ad + ab + 2 + 3.4"))
