"""
Αλγόριθμος του Dixon: ψάχνουμε X, Y με X^2 ≡ Y^2 (mod N), X ≢ ±Y,
οπότε gcd(X-Y, N) είναι μη τετριμμένος διαιρέτης του N.
"""

from math import gcd, isqrt


def primes_upto(B):
    """Οι πρώτοι <= B= factor base."""
    sieve = [True] * (B + 1)
    sieve[0:2] = [False, False]
    for i in range(2, isqrt(B) + 1):
        if sieve[i]:
            for j in range(i * i, B + 1, i):
                sieve[j] = False
    return [i for i, v in enumerate(sieve) if v]


def trial_division(r, base):
    """Δοκιμαστική διαίρεση: διάνυσμα εκθετών αν το r είναι B-smooth, αλλιώς None."""
    exps = [0] * len(base)
    for i, p in enumerate(base):
        while r % p == 0:
            r //= p
            exps[i] += 1
    return exps if r == 1 else None


def dixon(N, B, extra=5, verbose=True):
    base = primes_upto(B)
    k = len(base)

    # Βήμα 1: σχέσεις x^2 ≡ r (mod N) με r B-smooth
    relations = []  # (x, r, εκθέτες)
    x = isqrt(N) + 1
    while len(relations) < k + extra:
        r = (x * x) % N
        if r != 0:
            e = trial_division(r, base)
            if e is not None:
                relations.append((x, r, e))
        x += 1
        if x > N:
            return None
    if verbose:
        print(f"N={N}, B={B}, βάση={base}")
        for x_, r_, e_ in relations:
            print(f"  {x_}^2 mod N = {r_}  exps={e_}")

    # Βήμα 2: γραμμική άλγεβρα στο GF(2).
    # Κάθε σχέση -> bitmask με τις ισοτιμίες των εκθετών (mask) και
    # bitmask με τις σχέσεις που έχουμε συνδυάσει (comb).
    # Όταν μια γραμμή μηδενιστεί, ο συνδυασμός της έχει άρτιους εκθέτες παντού.
    rows = []
    for i, (_, _, e) in enumerate(relations):
        mask = sum((ei & 1) << j for j, ei in enumerate(e))
        rows.append((mask, 1 << i))
    pivots = {}
    deps = []
    for mask, comb in rows:
        while mask:
            low = mask & -mask
            if low in pivots:
                pm, pc = pivots[low]
                mask ^= pm
                comb ^= pc
            else:
                pivots[low] = (mask, comb)
                break
        if mask == 0:
            deps.append(comb)

    # Βήμα 3: X = γινόμενο των x, Y = τετραγωνική ρίζα του γινομένου των r
    for comb in deps:
        chosen = [relations[i] for i in range(len(relations)) if comb >> i & 1]
        X = 1
        total = [0] * k
        for x_, _, e_ in chosen:
            X = X * x_ % N
            total = [a + b for a, b in zip(total, e_)]
        Y = 1
        for p, t in zip(base, total):
            Y = Y * pow(p, t // 2, N) % N
        g = gcd(X - Y, N)
        if verbose:
            idx = [i for i in range(len(relations)) if comb >> i & 1]
            print(f"  εξάρτηση {idx}: X={X}, Y={Y}, gcd={g}")
        if 1 < g < N:  # αλλιώς X ≡ ±Y: δοκιμάζουμε την επόμενη εξάρτηση
            return g, N // g
    return None


if __name__ == "__main__":
    for N, B in [(58801, 11), (98069, 13), (84923, 13), (1649, 7), (10007 * 10009, 60)]:
        print("=>", dixon(N, B, verbose=(N < 100000)))
        print()
