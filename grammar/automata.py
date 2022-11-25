import os
import string
from grammar.tokenizer import tokenize_arithmetic


class DFAStateException(Exception):
    pass


def _check_states(states: set, transitions: dict, final_state: set):
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

    def process(self, input_str) -> bool:
        _check_states(self.states, self.transitions, self.final_state)
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


def check_name(input_str: str):
    # Check if input_str is not a reserved name in JavaScript
    with open(os.getcwd() + r"\grammar\reservedKeywords.txt") as f:
        reserved = f.read().splitlines()
    if input_str in reserved:
        return False

    # DFA Initialization
    states = {"q0", "q1"}
    alphabet = list(string.ascii_letters) + list(string.digits) + ["_", "$"]
    transitions = {**{("q0", p): "q1" for p in string.ascii_letters + "_" + "$"},
                   **{("q1", p): "q1" for p in string.ascii_letters + string.digits + "_" + "$"}}
    start_state = "q0"
    final_states = {"q1"}

    dfa = DFA(states, alphabet, transitions, start_state, final_states)

    return dfa.process(input_str)


def check_arithmetic(input_str: str) -> bool:
    operators = ["+", "++", "-", "--", "*", "/", "%", "&", "|", "^", "~", "<<", ">>", ">>>"]
    ternary = ["?", ":"]
    tokens = tokenize_arithmetic(input_str)
    variables = [v for t, v in tokens if t == "VAR"]
    ops = [v for t, v in tokens if t == "OP"]
    nums = [v for t, v in tokens if t == "NUM"]
    floats = [v for t, v in tokens if t == "FLOAT"]

    # The great filter
    for var in variables:
        if not check_name(var):
            return False
    for op in ops:
        if op not in operators + ternary:
            return False
    states = {"q0", "q1", "qt1", "qt2", "q2", "q3"}
    alphabet = variables + operators + nums + floats + ternary
    transitions = {**{("q0", p): "q1" for p in variables + nums + floats},
                   **{("q1", "?"): "qt1"},
                   **{("qt1", p): "qt2" for p in variables + nums + floats},
                   **{("qt2", ":"): "q2"},
                   **{("q1", p): "q2" for p in operators},
                   **{("q2", p): "q3" for p in variables + nums + floats},
                   **{("q3", p): "q2" for p in operators}}
    start_state = "q0"
    final_states = {"q3"}

    fa = DFA(states, alphabet, transitions, start_state, final_states)
    return fa.process((t[1] for t in tokens))


if __name__ == "__main__":
    print(check_arithmetic("a ? b : c"))
