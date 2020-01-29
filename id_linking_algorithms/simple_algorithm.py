from id_linking_algorithms.normalizer import normalizer


def start_simple_algorithm(users, vector=[]):
    I = []
    for user in users:
        temp = user
        temp["normalized"] = normalizer(user["email"])
        I.append(temp)
    return simple_algorithm(I, vector)


def simple_algorithm(I, vector):
    identityMerges = []
    p = 3  # similarity threshold
    if len(vector) == 0:
        while len(I) > 0:
            iMerge.append(I.pop(0))
            for i in I:
                if shouldInclude(iMerge, i, p):
                    iMerge.append(i)
                    I.remove(i)
            identityMerges.append(iMerge)
    else:
        identityMergesTemp = vector
        while len(I) > 0:
            iMerge = []
            if x < len(identityMergesTemp) and len(identityMergesTemp[x]) > 0:
                iMerge = identityMergesTemp[x].copy()
            else:
                iMerge.append(I.pop(0))
            for i in I:
                if shouldInclude(iMerge, i, p):
                    iMerge.append(i)
                    I.remove(i)
            identityMerges.append(iMerge)
            x += 1

        while len(I) > 0:
            for i in I:
                x = 0
                while True:
                    iMerge = []
                    if x < len(identityMergesTemp):
                        iMerge = identityMergesTemp[x].copy()

                    if shouldInclude(iMerge, i, p):
                        iMerge.append(i)
                        I.remove(i)
                        break

                    x += 1
                for iMergeTemp in identityMergesTemp:
                    iMerge = iMergeTemp.copy()
                    if shouldInclude(iMerge, i, p):
                        iMerge.append(i)
                        I.remove(i)
                        break
                identityMerges.append(iMerge)
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
