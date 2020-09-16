def run(shouldInclude, _i, p):
    id_counter = 1

    identityMerges = {}
    while len(_i) > 0:
        iMerge = {id_counter: []}
        iMerge[id_counter].append(_i.pop(0))
        for i in _i:
            if shouldInclude(iMerge, i, p):
                iMerge[id_counter].append(i)
                _i.remove(i)
        identityMerges.update(iMerge)
        id_counter += 1

    return identityMerges
