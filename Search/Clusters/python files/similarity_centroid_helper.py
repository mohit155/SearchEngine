import math


def dot_product(a, b):
    c = 0
    for x in a:
        if x in b:
            c += a[x]*b[x]
    return c


def magnitude(a):
    mag = 0
    for x in a:
        mag += a[x]*a[x]

    mag = math.sqrt(mag)
    return mag


def cosine_similarity(a, b):
    c = dot_product(a, b)
    mag_a = magnitude(a)
    mag_b = magnitude(b)
    sim = (c/mag_a)/mag_b
    return sim

l = {
    'one': {'a': 1, 'b': 2},
    'two': {'a': 3, 'b': 6}
}


def centroid(a):
    b = {}
    for vector in a:
        for token in a[vector]:
            if token not in b:
                b[token] = a[vector][token]
            else:
                b[token] += a[vector][token]
    for token in b:
        b[token] /= len(a)
    return b
