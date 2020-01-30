from id_linking_algorithms.normalizer import normalizer
from id_linking_algorithms.base_algorithm import base_algorithm


def start_simple_algorithm(users, maps_existent=[]):
    I = []
    for user in users:
        temp = user
        temp["normalized"] = normalizer(user["email"])
        I.append(temp)
    return simple_algorithm(I, maps_existent)


def simple_algorithm(I, maps_existent):
    return base_algorithm(I=I, maps_existent=maps_existent, shouldInclude=shouldInclude, p=0.3)


def shouldInclude(iMerge, i, p):
    check = False
    for x in list(iMerge.values())[0]:
        if i["normalized"] == x["normalized"]:
            check = True
            break
    if check and (len(i["normalized"]) > p):
        return True

    return False
