def run(should_include, _i, p):
    id_counter = 1

    identity_merges = {}
    while len(_i) > 0:
        i_merge = {id_counter: []}
        i_merge[id_counter].append(_i.pop(0))
        for i in _i[:]:
            if should_include(i_merge[id_counter], i, p):
                i_merge[id_counter].append(i)
                _i.remove(i)
        identity_merges.update(i_merge)
        id_counter += 1

    return identity_merges
