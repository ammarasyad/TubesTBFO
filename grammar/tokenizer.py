def isfloat(input_str: str) -> bool:
    if input_str is None:
        return False
    try:
        float(input_str)
        return True
    except ValueError:
        return False


def tokenize_arithmetic(input_str: str):
    operators = ["+", "++", "-", "--", "*", "/", "%", "&", "|", "^", "~", "<<", ">>", ">>>"]
    if " " in input_str:
        input_str = input_str.replace(" ", "")

    tokens = []
    var = ""
    for c in input_str:
        if c in operators:
            if var.isdigit():
                tokens.append(("NUM", var))
            elif isfloat(var):
                tokens.append(("FLOAT", var))
            else:
                tokens.append(("VAR", var))
            var = ""
            tokens.append(("OP", c))
            continue
        var += c
    if var.isdigit():
        tokens.append(("NUM", var))
    elif isfloat(var):
        tokens.append(("FLOAT", var))
    else:
        tokens.append(("VAR", var))
    # Cleanup the tokens
    tokens = [(t, v) for t, v in tokens if v != ""]

    return tokens


if __name__ == "__main__":
    # Buat testing
    print(tokenize_arithmetic("$var1 + 123.3.38"))
# g = tokenize.tokenize(BytesIO("$var1 + $var2 = 3".encode("utf-8")).readline)
# print(next(g))
# print(type(next(g)))
