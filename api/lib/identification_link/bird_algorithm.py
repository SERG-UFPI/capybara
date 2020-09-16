from . import base_algorithm, normalizer


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def start_bird_algorithm(users):
    _i = []
    for user in users:
        temp = user
        temp["normalized"] = normalizer.run(user["email"])
        _i.append(temp)
    return bird_algorithm(_i)


def bird_algorithm(_i):
    return base_algorithm.run(_i=_i, shouldInclude=shouldInclude, p=0.3)


matriz = {}


def shouldInclude(iMerge, i, p):
    check = False
    for x in list(iMerge.values())[0]:
        value = None
        if ((i["normalized"], x["normalized"])) in matriz:
            value = matriz[(i["normalized"], x["normalized"])]
        else:
            size_1 = len(i["normalized"])
            size_2 = len(x["normalized"])
            if size_1 == 0 and size_2 == 0:
                continue
            value = 1 - (levenshtein(i["normalized"], x["normalized"])) / (
                max([size_1, size_2])
            )
            matriz[(i["normalized"], x["normalized"])] = value
        if value >= p:
            check = True
            break

    return check
