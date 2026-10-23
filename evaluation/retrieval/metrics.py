"""Retrieval metrics.

A chunk is correct when its (file, page) is in the question's `relevant` list.
`retrieved` is the list of (file, page) of the returned chunks, best first.

    Hit Rate : 1 if at least one relevant page is retrieved, else 0
    MRR      : 1 / rank of the first relevant chunk (0 if none)
"""


def hit_rate(retrieved, relevant):
    return 1.0 if any(c in relevant for c in retrieved) else 0.0


def mrr(retrieved, relevant):
    for rank, c in enumerate(retrieved, start=1):
        if c in relevant:
            return 1 / rank
    return 0.0
