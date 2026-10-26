
from math import isqrt


def sieve_primes(limit):
    """Επιστρέφει όλους τους πρώτους αριθμούς μέχρι το limit."""
    if limit < 2:
        return []

    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    for p in range(2, isqrt(limit) + 1):
        if is_prime[p]:
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False

    return [n for n in range(2, limit + 1) if is_prime[n]]


def find_prime_values(C, x_start, x_end):
    """Εντοπίζει τις τιμές Q(x) = x² - C με πρώτης τάξης απόλυτη τιμή."""

    values = [(x, x * x - C) for x in range(x_start, x_end + 1)]

    # Μέγιστη απόλυτη τιμή του πολυωνύμου
    limit = max(abs(q) for x, q in values)

    # Δημιουργία πίνακα πρώτων αριθμών
    primes = set(sieve_primes(limit))

    print(f"Πολυώνυμο: Q(x) = x² - {C}")
    print(f"Διάστημα: [{x_start}, {x_end}]")
    print("\nΤιμές του πολυωνύμου:")

    for x, q in values:
        if abs(q) in primes:
            print(f"x = {x:2}, Q(x) = {q:4} --> |Q(x)| = {abs(q)} είναι πρώτος")
        else:
            print(f"x = {x:2}, Q(x) = {q:4} --> |Q(x)| = {abs(q)} δεν είναι πρώτος")


# Παράδειγμα της άσκησης
C = int(input("Δώσε την τιμή C: "))
x_start = int(input("Δώσε την αρχή του διαστήματος: "))
x_end = int(input("Δώσε το τέλος του διαστήματος: "))

find_prime_values(C, x_start, x_end)


# Τροποποίηση του Sieve:
# Αντί να εντοπίζουμε B-smooth αριθμούς,
# βρίσκουμε όλους τους πρώτους,
# μέχρι τη μέγιστη απόλυτη τιμή του Q(x) στο επιλεγμένο
# διάστημα. Στη συνέχεια, ελέγχουμε ποιες τιμές του Q(x)
# έχουν απόλυτη τιμή που ανήκει στο σύνολο των πρώτων αριθμών.
# Έτσι, ο αλγόριθμος μπορεί να εφαρμοστεί σε διαφορετικές
# τιμές της σταθεράς C και σε διαφορετικά διαστήματα του x.