def while_do(lines):
    for i, line in enumerate(lines):
        temp = ""
        var = ""
        flag = False
        app = 0

        # Handling while loops
        if line.startswith("while") or line.startswith("\twhile"):
            lines[i] = line.rstrip() + ":"

        # Handling i++, i--
        for j in range(len(line)):
            if line[j] == "+" and line[j + 1] == "+":
                line = line[:j + 1] + "=1" + line[j + 2:]
            elif line[j] == "-" and line[j + 1] == "-":
                line = line[:j + 1] + "=1" + line[j + 2:]

        # Handling do-while loops
        if line.strip().endswith("} while"):
            flag = True
            app = line.count("\t")

        if flag:
            condition = line[app * "\t".__len__() + 7:].rstrip("}")
            for ch in condition:
                if ch == "<=":
                    temp += "> "
                    break
                elif ch == ">=":
                    temp += "< "
                    break
                elif ch == "<":
                    temp += ">= "
                elif ch == ">":
                    temp += "<= "
                elif ch == "==":
                    temp += "!= "
                elif ch == "!=":
                    temp += "== "
                else:
                    temp += ch
            temp += ": break"
            line = "\t" * app + "if " + temp

        # Handling do-while loops
        if line.strip() == "do":
            line = "while True:"
        else:
            line = line.replace("do", "while True:")

        lines[i] = line

    return lines


# Example usage:
code = [
    "while (condition) {",
    "\tstatements;",
    "}",
    "do {",
    "\tstatements;",
    "} while (condition);"
]

translated_code = while_do(code)
for line in translated_code:
    print(line)
