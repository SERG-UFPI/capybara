from id_linking_algorithms.normalizer import normalizer

id_counter = 1


def start_simple_algorithm(users, maps_existent=[], users_existent=[]):
    I = []
    for user in users:
        temp = user
        # print(temp)
        temp["normalized"] = normalizer(user["email"])
        I.append(temp)
    return simple_algorithm(I, maps_existent, users_existent)


def simple_algorithm(I, maps_existent, users_existent):
    global id_counter
    identityMerges = []
    p = 3  # similarity threshold
    if len(maps_existent) == 0:
        while len(I) > 0:
            iMerge = {id_counter: []}
            iMerge[id_counter].append(I.pop(0))
            for i in I:
                if shouldInclude(iMerge[id_counter], i, p):
                    iMerge[id_counter].append(i)
                    I.remove(i)
            identityMerges.append(iMerge)
            id_counter += 1
    else:
        index_map_existent = 0
        identityMergesTemp = maps_existent
        # print(f"identityMergesTemp ==> {identityMergesTemp}")
        while len(I) > 0:
            for iMergeTemp in identityMergesTemp:
                id_counter = list(iMergeTemp.keys())[0]
                iMerge = iMergeTemp[id_counter]
                for i in I:
                    if shouldInclude(iMerge, i, p):
                        iMerge[id_counter].append(i)
                        I.remove(i)
            id_counter += 1
            iMerge = {id_counter: []}
            iMerge[id_counter].append(I.pop(0))
            for i in I:
                if shouldInclude(iMerge[id_counter], i, p):
                    iMerge[id_counter].append(i)
                    I.remove(i)
            identityMerges.append(iMerge)
            id_counter += 1
        identityMerges = identityMergesTemp.copy()

    return identityMerges


def shouldInclude(iMerge, i, p):
    check = False
    for x in iMerge:
        if i["normalized"] in x.values():
            check = True
            break
    if check and (len(i["normalized"]) > p):
        return True

    return False
