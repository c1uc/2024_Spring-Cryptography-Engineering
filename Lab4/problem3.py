import numpy as np
import matplotlib.pyplot as plt
import itertools

rng = np.random.default_rng()


def naive_shuffle(A):
    n = len(A)
    for i in range(n):
        j = rng.integers(n)
        A[i], A[j] = A[j], A[i]
    return A


def fisher_yates_shuffle(A):
    n = len(A)
    for i in range(n - 1, 0, -1):
        j = rng.integers(i + 1)
        A[i], A[j] = A[j], A[i]
    return A


def main():
    N = 1000000
    naive = dict()
    fisher = dict()

    [naive.setdefault(_, 0) for _ in itertools.permutations(range(1, 5))]
    [fisher.setdefault(_, 0) for _ in itertools.permutations(range(1, 5))]

    for _ in range(N):
        naive[tuple(naive_shuffle([1, 2, 3, 4]))] += 1
        fisher[tuple(fisher_yates_shuffle([1, 2, 3, 4]))] += 1

    plt.plot([''.join(map(str, _)) for _ in naive.keys()], list(naive.values()), alpha=0.5, c='b', label="Naive")
    plt.plot([''.join(map(str, _)) for _ in fisher.keys()], list(fisher.values()), alpha=0.5, c='r', label="Fisher-Yates")
    plt.xticks(rotation=90)
    plt.title("Naive vs Fisher-Yates")
    plt.legend()
    plt.savefig("lab4_problem3.png")
    plt.show()

    print("Naive:")
    [print(f"{_}: {naive[_]}") for _ in naive.keys()]

    print("Fisher-Yates:")
    [print(f"{_}: {fisher[_]}") for _ in fisher.keys()]


if __name__ == "__main__":
    main()
