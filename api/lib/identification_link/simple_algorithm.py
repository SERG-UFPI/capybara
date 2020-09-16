from . import base_algorithm, normalizer


def start_simple_algorithm(users):
    _i = []
    for user in users:
        temp = user
        temp["normalized"] = normalizer.run(user["email"])
        _i.append(temp)
    return simple_algorithm(_i)


def simple_algorithm(_i):
    return base_algorithm.run(_i=_i, shouldInclude=shouldInclude, p=0.3)


def shouldInclude(iMerge, i, p):
    check = False
    for x in list(iMerge.values())[0]:
        if i["normalized"] == x["normalized"]:
            check = True
            break
    if check and (len(i["normalized"]) > p):
        return True

    return False
