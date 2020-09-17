from api.lib.identification_link import normalizer
from api.lib.identification_link import base_algorithm


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # j+1 instead of j since previous_row and current_row are one character longer
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def start_improved_algorithm(users):
    print(users)
    _i = []
    for user in users:
        temp = user
        temp["normalized_email"] = normalizer.run(user["email"])
        temp["normalized_name"] = normalizer.run(user["name"])
        _i.append(temp)
    return improved_algorithm(_i)


def improved_algorithm(_i):
    return base_algorithm.run(_i=_i, should_include=should_include, p=1.0)


def teste1(iMerge, i, p):
    check = False
    for x in iMerge:
        size_1 = len(i["normalized_name"])
        size_2 = len(x["normalized_email"])
        if size_1 == 0 and size_2 == 0:
            continue
        if (
            1
            - (levenshtein(i["normalized_name"], x["normalized_email"]))
            / (max([size_1, size_2]))
            >= p
        ):
            check = True
            break

    return check


def teste2(iMerge, i, p):
    characters = ["+", ".", "-", "_"]

    for x in iMerge:
        label1 = x["name"]
        label2 = i["name"]

        for char in characters:
            label1 = label1.replace(char, " ")
            label2 = label2.replace(char, " ")

        label1_splited = label1.split(" ")
        label2_splited = label2.split(" ")

        result = list(filter(lambda x: not x in label2_splited, label1_splited))

    return len(result) == 0


def teste3(iMerge, i, p):
    check = False
    for x in iMerge:
        size_1 = len(i["normalized_name"])
        size_2 = len(x["normalized_name"])
        if size_1 == 0 and size_2 == 0:
            continue
        if (
            1
            - (levenshtein(i["normalized_name"], x["normalized_name"]))
            / (max([size_1, size_2]))
            >= p
        ):
            check = True
            break

    return check


def permutation(lst):
    if len(lst) == 0:
        return []
    if len(lst) == 1:
        return [lst]
    l = []
    for i in range(len(lst)):
        m = lst[i]
        remLst = lst[:i] + lst[i + 1 :]
        for p in permutation(remLst):
            l.append([m] + p)
    return l


def combination(*args, repeat=1):
    pools = [list(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x + [y] for x in result for y in pool]
    for prod in result:
        yield list(prod)


def teste4(iMerge, i, p):
    characters = ["+", ".", "-", "_"]

    for x in iMerge:
        label1 = x["name"]
        label2 = i["normalized_email"]

        for char in characters:
            label1 = label1.replace(char, " ")

        label1_splited = label1.split(" ")
        permut = permutation(label1_splited)

        prefix_possible = []
        for p in permut:
            aux = list(combination(characters, repeat=(len(p) - 1)))
            for item in aux:
                prefix_possible.append(
                    "".join(val for pair in zip(p, item + [""]) for val in pair)
                )
        return label2 in prefix_possible


def should_include(iMerge, i, p):
    functions = [teste1, teste2, teste3, teste4]

    for function in functions:
        if function(iMerge, i, p):
            return True
    return False
