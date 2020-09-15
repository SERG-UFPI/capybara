def run(shouldInclude, I, p):
    id_counter = 1

    identityMerges = {}
    while len(I) > 0:
        iMerge = {id_counter: []}
        iMerge[id_counter].append(I.pop(0))
        for i in I:
            if shouldInclude(iMerge, i, p):
                iMerge[id_counter].append(i)
                I.remove(i)
        identityMerges.update(iMerge)
        id_counter += 1

    return identityMerges
