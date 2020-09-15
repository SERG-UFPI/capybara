from . import normalizer
from . import base_algorithm


def start_simple_algorithm(users):
    I = []
    for user in users:
        temp = user
        temp["normalized"] = normalizer.run(user["email"])
        I.append(temp)
    return simple_algorithm(I)


def simple_algorithm(I):
    return base_algorithm.run(I=I, shouldInclude=shouldInclude, p=0.3)


def shouldInclude(iMerge, i, p):
    check = False
    for x in list(iMerge.values())[0]:
        if i["normalized"] == x["normalized"]:
            check = True
            break
    if check and (len(i["normalized"]) > p):
        return True

    return False
