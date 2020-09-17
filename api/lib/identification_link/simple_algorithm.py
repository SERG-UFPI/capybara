from . import base_algorithm, normalizer


def start_simple_algorithm(users):
    _i = []
    for user in users:
        temp = user
        temp["normalized"] = normalizer.run(user["email"])
        _i.append(temp)
    return simple_algorithm(_i)


def simple_algorithm(_i):
    return base_algorithm.run(_i=_i, should_include=should_include, p=1.0)


def should_include(iMerge, i, p):
    check = False
    for x in iMerge:
        i_normalized = i.get("normalized", None)
        x_normalized = x.get("normalized", None)

        if (i_normalized and x_normalized) and i_normalized == x_normalized:
            check = True
            break
    if check and (len(i_normalized) > p):
        return True
    return False
