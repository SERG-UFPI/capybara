id_counter = 1


def base_algorithm(shouldInclude, maps_existent, I, p):
    global id_counter
    identityMerges = []
    if len(maps_existent) == 0:
        while len(I) > 0:
            iMerge = {id_counter: []}
            iMerge[id_counter].append(I.pop(0))
            for i in I:
                if shouldInclude(iMerge, i, p):
                    iMerge[id_counter].append(i)
                    I.remove(i)
            identityMerges.append(iMerge)
            id_counter += 1
    else:
        maps_existent_sorted = sorted(
            maps_existent, key=lambda k: list(k.keys())[0])
        identityMergesTemp = maps_existent_sorted
        for iMergeTemp in identityMergesTemp:
            id_counter = list(iMergeTemp.keys())[0]
            iMerge = iMergeTemp.copy()
            for i in I:
                if shouldInclude(iMerge, i, p):
                    iMerge[id_counter].append(i)
                    I.remove(i)
            identityMerges.append(iMerge)
        id_counter += 1
        while len(I) > 0:
            iMerge = {id_counter: []}
            iMerge[id_counter].append(I.pop(0))
            for i in I:
                if shouldInclude(iMerge, i, p):
                    iMerge[id_counter].append(i)
                    I.remove(i)
            identityMerges.append(iMerge)
            id_counter += 1

    return identityMerges
