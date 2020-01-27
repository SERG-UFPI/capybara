from id_linking_algorithms.normalizer import normalizer


def start_simple_algorithm(users, vector=[]):
    I = []
    for user in users:
        normalized_user = normalizer(user["email"])
        I.append(normalized_user)
    return simple_algorithm(I, vector)


def simple_algorithm(I, vector):
    identityMerges = []
    p = 3  # similarity threshold
    if len(vector) == 0:
        while len(I) > 0:
            r = I[0]  # First element from I
            iMerge = []
            iMerge.append(r)
            I.remove(r)
            for i in I:
                if shouldInclude(iMerge, i, p):
                    iMerge.append(i)
                    I.remove(i)
            identityMerges.append(iMerge)
    else:
        identityMergesTemp = vector
        while len(I) > 0:
            for i in I:
                for iMergeTemp in identityMergesTemp:
                    iMerge = iMergeTemp.copy()
                    if shouldInclude(iMerge, i, p):
                        iMerge.append(i)
                        I.remove(i)
                        break
                identityMerges.append(iMerge)
    return identityMerges


def shouldInclude(iMerge, i, p):
    if (i in iMerge) and (len(i) > p):
        return True

    return False
