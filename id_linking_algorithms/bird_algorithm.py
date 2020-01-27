from id_linking_algorithms.normalizer import normalizer


def start_bird_algorithm(users, vector=[]):
    I = []
    for user in users:
        normalized_user = normalizer(user["email"])
        I.append(normalized_user)
    return bird_algorithm(I, vector)


def bird_algorithm(I, vector):
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
    if not a:
        return len(b)
    if not b:
        return len(a)
    result = min(lev(a[1:], b[1:])+(a[0] != b[0]),
                 lev(a[1:], b)+1, lev(a, b[1:])+1)
    if result >= p:
        return True

    return False
