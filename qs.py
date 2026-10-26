from math import isqrt, gcd


def quadratic_sieve(N, B=50, max_steps=200000):
    # Έλεγχος εισόδου
    if not isinstance(N, int) or N < 2:
        raise ValueError("Το N πρέπει να είναι ακέραιος >= 2")

    # Έλεγχος για εύκολους παράγοντες
    if N % 2 == 0:
        return 2, N // 2

    for p in range(3, isqrt(N) + 1, 2):
        if N % p == 0:
            return p, N // p

    # Δημιουργία πρώτων αριθμών μέχρι το B
    sieve = [True] * (B + 1)
    sieve[0] = sieve[1] = False

    for p in range(2, isqrt(B) + 1):
        if sieve[p]:
            for j in range(p * p, B + 1, p):
                sieve[j] = False

    primes = [p for p in range(2, B + 1) if sieve[p]]

    # Δημιουργία βάσης παραγόντων
    base = []

    for p in primes:
        if N % p == 0:
            return p, N // p

        if p == 2 or pow(N % p, (p - 1) // 2, p) == 1:
            base.append(p)

    # Αποθήκευση των B-smooth σχέσεων
    relations = []
    linear_basis = {}

    x = isqrt(N) + 1

    for _ in range(max_steps):
        value = x * x - N
        remaining = value
        exponents = [0] * len(base)

        # Παραγοντοποίηση ως προς τη βάση
        for i, p in enumerate(base):
            while remaining % p == 0:
                remaining //= p
                exponents[i] += 1

        # Κρατάμε μόνο τις B-smooth τιμές
        if remaining == 1:
            parity = 0

            for i, e in enumerate(exponents):
                if e % 2:
                    parity |= 1 << i

            index = len(relations)
            relations.append((x, exponents, parity))

            # Γραμμική άλγεβρα πάνω από GF(2)
            mask = parity
            combination = 1 << index

            while mask:
                pivot = mask.bit_length() - 1

                if pivot not in linear_basis:
                    linear_basis[pivot] = (mask, combination)
                    break

                old_mask, old_combination = linear_basis[pivot]
                mask ^= old_mask
                combination ^= old_combination

            # Βρέθηκε γραμμική εξάρτηση
            if mask == 0:
                X = 1
                exponent_sums = [0] * len(base)

                for j, (rx, re, _) in enumerate(relations):
                    if (combination >> j) & 1:
                        X = (X * rx) % N

                        for k, e in enumerate(re):
                            exponent_sums[k] += e

                # Οι συνολικοί εκθέτες πρέπει να είναι άρτιοι
                if all(e % 2 == 0 for e in exponent_sums):
                    Y = 1

                    for p, e in zip(base, exponent_sums):
                        Y = (Y * pow(p, e // 2, N)) % N

                    # Εύρεση παραγόντων με ΜΚΔ
                    for d in (gcd(X - Y, N), gcd(X + Y, N)):
                        if 1 < d < N:
                            return d, N // d

        x += 1

    return None


# εκτέλεση με εισοδο απο τον χρηστη
N = int(input("Δώσε έναν ακέραιο αριθμό N: "))

result = quadratic_sieve(N, B=50)

if result:
    print("Οι παράγοντες του", N, "είναι:", result)
else:
    print("Δεν βρέθηκαν παράγοντες με τις συγκεκριμένες παραμέτρους.")