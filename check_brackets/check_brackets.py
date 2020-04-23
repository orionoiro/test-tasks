def check_with_oddness(string):
    if len(string) % 2 != 0:
        return False
    else:
        return check_brackets(string)


def check_brackets(string):
    complete = {'(': ')', '[': ']', '{': '}'}

    if string:
        for idx, elem in enumerate(string):
            if elem in complete:
                if complete[elem] == string[idx + 1]:
                    return check_brackets(string[:idx] + string[idx + 2:])
    else:
        return True
    return False

