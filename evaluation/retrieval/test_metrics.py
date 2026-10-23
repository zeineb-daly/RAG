"""Small examples whose expected scores are computed by hand.

Run from the ESILV_Tutor folder:
    python -m evaluation.retrieval.test_metrics
"""
from evaluation.retrieval.metrics import hit_rate, mrr

A, B, C = ("a.pdf", 1), ("a.pdf", 2), ("b.pdf", 1)

assert hit_rate([A, B, C], {A}) == 1 and mrr([A, B, C], {A}) == 1          # rank 1
assert hit_rate([B, A, C], {A}) == 1 and mrr([B, A, C], {A}) == 1 / 2      # rank 2
assert hit_rate([B, C], {A}) == 0 and mrr([B, C], {A}) == 0                # miss
assert hit_rate([("b.pdf", 1)], {("a.pdf", 1)}) == 0                       # same page, other file

print("All metric tests passed")
