import string
from timeit import timeit


class FAStateException(Exception):
    pass


def check_states(states: set, transitions: dict, final_state: set):
    # Check if transition states and final states are in states
    # I'm pretty sure this is not needed, but I love over-engineering
    # I LOVE READABLE CODE!!!!!!
    no_states = []
    for fstate in final_state:
        if fstate not in states:
            no_states.append(fstate)
    if no_states:
        raise FAStateException(
            f"Final {'states' if len(no_states) > 1 else 'state'} {', '.join(no_states)} {'are' if len(no_states) > 1 else 'is'} not in states")
    no_states.clear()
    for key, value in transitions.items():
        if key[0] not in states:
            no_states.append(key[0])
        if value not in states:
            no_states.append(value)
    if no_states:
        raise FAStateException(
            f"Transition {'states' if len(no_states) > 1 else 'state'} {', '.join(no_states)} {'are' if len(no_states) > 1 else 'is'} not in states")


class FA:
    def __init__(self, states: set, alphabet: list, transitions: dict, start_state: str, final_state: set):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_state = final_state

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
                print(f"Transition from {current_state} with {c} is not defined")
                return False
        return current_state in self.final_state


# class NFA(FA):
#     def __init__(self, states: set, alphabet: list, transitions: dict, start_state: str, final_state: set):
#         super().__init__(states, alphabet, transitions, start_state, final_state)
#         self.epsilon_states = set()
#         for key, value in self.transitions.items():
#             if key[1] == "e":
#                 self.epsilon_states.add(key[0])
#                 self.epsilon_states.add(value)
#
#     def process(self, input_str: str) -> bool:
#         check_states(self.states, self.transitions, self.final_state)


def check_name(input_str: str):
    # Check if input_str is not a reserved name in JavaScript
    with open("reservedKeywords.txt") as f:
        reserved = f.read().splitlines()
    if input_str in reserved:
        return False

    # (D)FA Initialization
    states = {"q0", "q1"}
    alphabet = list(string.ascii_letters) + list(string.digits) + ["_"]
    # transitions = {
    #     ("q0", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"): "q1",
    #     ("q1", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"): "q1"
    # }
    transitions = {**{("q0", p): "q1" for p in string.ascii_letters + "_"},
                   **{("q1", p): "q1" for p in string.ascii_letters + string.digits + "_"}}
    start_state = "q0"
    final_states = {"q1"}

    fa = FA(states, alphabet, transitions, start_state, final_states)

    return fa.process(input_str)


# TODO: Refine this, minimize the states if possible, and check for edge cases
def check_arithmetic(input_str: str) -> bool:
    # No ternary operators because that is hard
    operators = ["+", "-", "*", "/", "%", "++", "--", "(", ")"]
    secondary_ops = ["=", "+=", "-=", "*=", "/=", "%=", "==", "!=", ">", "<", ">=", "<=", "===", "!==", ";"]
    # filtered = [c for c in input_str.split() if c not in operators]
    # for f in filtered:
    #     if not f.isdigit():
    #         print(check_name(f))
    states = {"q0", "q1", "q2", "q3", "q4"}
    alphabet = list(string.ascii_letters) + list(string.digits) + operators + secondary_ops + ["_", " "]
    # Pseudo NFA transition states?
    transitions = {**{("q0", p): "q0" for p in string.ascii_letters + string.digits + "(" + " "},
                   **{("q0", p): "q1" for p in operators},
                   **{("q1", p): "q1" for p in string.ascii_letters + string.digits + " "},
                   **{("q1", p): "q2" for p in string.ascii_letters + string.digits + ''.join(operators)},
                   **{("q1", p): "q3" for p in secondary_ops},
                   **{("q2", p): "q1" for p in string.ascii_letters + string.digits + ")" + " "},
                   **{("q2", p): "q3" for p in secondary_ops},
                   **{("q3", p): "q4" for p in alphabet}}
    start_state = "q0"
    final_states = {"q2", "q3"}

    fa = FA(states, alphabet, transitions, start_state, final_states)

    return fa.process(input_str)


print(check_arithmetic("a + b + c + d / e * f % g"))
