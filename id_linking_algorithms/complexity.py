import Levenshtein as lev
from datetime import timedelta
import time


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


if __name__ == "__main__":
    s1 = "maxnicolasdeoliveiralima"
    s2 = "m4xn1c0l4ste0l1veiral1m4"
    init1 = time.time()
    a = lev.distance(s1, s2)
    end1 = time.time()
    result1 = end1 - init1

    init2 = time.time()
    b = levenshtein(s1, s2)
    end2 = time.time()
    result2 = end2 - init2

    print(f"Algoritmo oficial: {result1} secs | Result: {a}")
    print(f"Algoritmo comunidade: {result2} secs | Result: {b}")

    # print(
    #     f"Algoritmo oficial: {timedelta(milliseconds=round(result1))} secs (Wall clock time)"
    # )
    # print(
    #     f"Algoritmo comunidade: {timedelta(milliseconds=round(result2))} secs (Wall clock time)"
    # )
