
from classes import TFN, scalar_product, fuzzy_distance


from pso_fcm_reasoning import sep



def aggregate_decision_makers(matrices: list[list[list[TFN]]]):
    K = len(matrices)
    m = len(matrices[0])
    n = len(matrices[0][0])

    X = [[None]*n for _ in range(m)]

    for i in range(m):
        for j in range(n):
            a = sum(matrices[k][i][j].a for k in range(K)) / K
            b = sum(matrices[k][i][j].b for k in range(K)) / K
            c = sum(matrices[k][i][j].c for k in range(K)) / K
            X[i][j] = TFN(a, b, c)

    return X



def print_fuzzy_matrix(M,decimals=3):

    rows = len(M)
    cols = len(M[0])

    for i in range(rows):
        row_str = []
        for j in range(cols):

            t = M[i][j]

            a = f"{t.a:.{decimals}f}"
            b = f"{t.b:.{decimals}f}"
            c = f"{t.c:.{decimals}f}"

            row_str.append(f"({a}, {b}, {c})")

        print("  ".join(row_str))

    print()

def fuzzy_topsis(X, W, benefit_criteria):


    m = len(X)        # alternative
    n = len(X[0])     # criteri
    print("m:",m)
    print("n:",n)

    # ==============================
    # STEP 2 – Normalizzazione
    # ==============================

    R = [[TFN(0,0,0)]*n for _ in range(m)]


    for j in range(n):

        if benefit_criteria[j]:  # J ∈ B
            max_c = max(X[i][j].c for i in range(m))

            for i in range(m):
                R[i][j] = TFN(
                    X[i][j].a / max_c,
                    X[i][j].b / max_c,
                    X[i][j].c / max_c
                )

        else:  # J ∈ C
            min_a = min(X[i][j].a for i in range(m))

            for i in range(m):
                R[i][j] = TFN(
                    min_a / X[i][j].c,
                    min_a / X[i][j].b,
                    min_a / X[i][j].a
                )


    sep()
    print("Normalized Fuzzy Decision Matrix")
    print_fuzzy_matrix(R)

    # ==============================
    # STEP 3 – Matrice Pesata
    # ==============================


    V = [[scalar_product(R[i][j],W[j]) for j in range(n) ] for i in range(m)]
    for i in range(m):
        for j in range(n):
            V[i][j].a = float(V[i][j].a)
            V[i][j].b = float(V[i][j].b)
            V[i][j].c = float(V[i][j].c)

    sep()
    print("Weighted Fuzzy Decision Matrix")
    print_fuzzy_matrix(V)


    # ==============================
    # STEP 4 – FPIS e FNIS
    # ==============================

    A_plus = []
    A_minus = []

    for j in range(n):

        max_a = max(V[i][j].a for i in range(m))
        max_b = max(V[i][j].b for i in range(m))
        max_c = max(V[i][j].c for i in range(m))

        min_a = min(V[i][j].a for i in range(m))
        min_b = min(V[i][j].b for i in range(m))
        min_c = min(V[i][j].c for i in range(m))

        A_plus.append(TFN(max_a, max_b, max_c))
        A_minus.append(TFN(min_a, min_b, min_c))

    sep()

    print("Soluzione ideale positiva")

    print(A_plus)
    sep()
    print("Soluzione ideale negativa")
    print(A_minus)

    sep()


    # ==============================
    # STEP 5 – Distanze
    # ==============================

    d_plus = []
    d_minus = []

    for i in range(m):

        dist_plus = 0
        dist_minus = 0

        for j in range(n):

            dist_plus += fuzzy_distance(V[i][j], A_plus[j])

            dist_minus += fuzzy_distance(V[i][j], A_minus[j])


        d_plus.append(dist_plus)
        d_minus.append(dist_minus)

    sep()
    print("Distance +")
    print(d_plus)
    print("Distance -")
    print(d_minus)
    sep()



    # ==============================
    # STEP 6 – Relative Closeness
    # ==============================

    RC = []

    for i in range(m):

        # RC_i = d_i^- / (d_i^+ + d_i^-)
        rc = d_minus[i] / (d_plus[i] + d_minus[i])
        RC.append(rc)

    # ==============================
    # STEP 7 – Ranking
    # ==============================

    ranking = sorted(
        [(i+1, RC[i]) for i in range(m)],
        key=lambda x: x[1],
        reverse=True
    )



    return RC, ranking




def print_results(RC, ranking):
    labels = ["A", "B", "C", "D", "E"]

    print("Relative Closeness:")
    for i, val in enumerate(RC):
        print(f"{labels[i]}: {val:.4f}")

    print("\nRanking Finale:")
    for alt, score in ranking:
        print(f"Fornitore {labels[alt - 1]} → {score:.4f}")




