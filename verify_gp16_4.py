"""Exact verification of the straight-line certificate, Python 3, standard library."""
from itertools import combinations
from pathlib import Path
import json


def det(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])


def verify(cert):
    if any(len(cert[s]) != 16 for s in ("u", "v")):
        raise ValueError("Expected 16 + 16 vertices")
    P = cert["u"] + cert["v"]
    if any(len(p) != 2 or any(type(c) is not int for c in p) for p in P):
        raise ValueError("Expected pairs of exact integers")
    if any(det(a,b,c) == 0 for a,b,c in combinations(P,3)):
        raise ValueError("Coincident vertices or a collinear triple")
    E = ([(i, (i+1)%16) for i in range(16)] +
         [(i, i+16) for i in range(16)] +
         [(16+i, 16+(i+4)%16) for i in range(16)])
    cross, counts, independent = [], [0]*len(E), 0
    for (i,(a,b)),(j,(c,d)) in combinations(enumerate(E),2):
        if len({a,b,c,d}) != 4:
            continue
        independent += 1
        if (det(P[a],P[b],P[c])*det(P[a],P[b],P[d]) < 0 and
            det(P[c],P[d],P[a])*det(P[c],P[d],P[b]) < 0):
            cross.append([i,j])
            counts[i] += 1
            counts[j] += 1
    if cross != cert["crossing_edge_ids"] or max(counts) != 1:
        raise ValueError((cross,counts))
    return E, cross, independent, counts


if __name__ == "__main__":
    cert = json.loads(Path(__file__).with_name("gp16-4-certificate.json").read_text("utf-8"))
    edges, pairs, independent, counts = verify(cert)
    print(f"32 vertices, {len(edges)} edges, 4960 noncollinear triples")
    print(f"{independent} disjoint-endpoint edge pairs; proper crossings: {pairs}")
    print(f"uncrossed={counts.count(0)}, crossed_once={counts.count(1)}, maximum={max(counts)}")

