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


def start_bird_algorithm(users):
    I = []
    for user in users:
        temp = user
        temp["normalized"] = normalizer.run(user["email"])
        I.append(temp)
    return bird_algorithm(I)


def bird_algorithm(I):
    return base_algorithm.run(_i=I, should_include=should_include, p=1.0)


def should_include(iMerge, i, p):
    check = False
    for x in iMerge:
        size_1 = len(i["normalized"])
        size_2 = len(x["normalized"])
        if size_1 == 0 and size_2 == 0:
            continue
        value = 1 - (levenshtein(i["normalized"], x["normalized"])) / (
            max([size_1, size_2])
        )
        if value >= p:
            check = True
            break

    return check
