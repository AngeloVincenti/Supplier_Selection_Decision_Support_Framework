
from classes import *




def load_fuzzy_decision_matrix():
    X = [
        [TFN(5, 8, 9), TFN(1, 1, 3), TFN(5, 8, 9), TFN(5, 8, 9), TFN(5, 7, 9),
         TFN(7, 9, 9), TFN(7, 9, 9), TFN(7, 9, 9), TFN(5, 8, 9), TFN(7, 9, 9),
         TFN(5, 8, 9), TFN(7, 9, 9), TFN(7, 9, 9), TFN(5, 8, 9), TFN(7, 9, 9),
         TFN(5, 8, 9), TFN(5, 8, 9), TFN(5, 8, 9)],

        [TFN(5, 7, 9), TFN(1, 2, 5), TFN(5, 7, 9), TFN(5, 7, 9), TFN(5, 7, 9),
         TFN(3, 6, 9), TFN(3, 5, 7), TFN(5, 8, 9), TFN(5, 7, 9), TFN(5, 7, 9),
         TFN(3, 6, 7), TFN(5, 7, 9), TFN(5, 7, 9), TFN(5, 7, 9), TFN(5, 8, 9),
         TFN(5, 7, 9), TFN(5, 7, 9), TFN(5, 7, 9)],

        [TFN(5, 8, 9), TFN(1, 2, 5), TFN(5, 8, 9), TFN(3, 7, 9), TFN(3, 5, 7),
         TFN(5, 7, 9), TFN(5, 7, 9), TFN(5, 7, 9), TFN(3, 6, 9), TFN(3, 6, 7),
         TFN(5, 7, 9), TFN(5, 7, 9), TFN(5, 7, 9), TFN(3, 6, 7), TFN(3, 6, 7),
         TFN(5, 7, 9), TFN(3, 6, 7), TFN(5, 7, 9)],

        [TFN(5, 7, 9), TFN(1, 1, 3), TFN(5, 8, 9), TFN(3, 6, 9), TFN(1, 4, 5),
         TFN(3, 6, 7), TFN(3, 6, 7), TFN(3, 5, 7), TFN(1, 4, 5), TFN(3, 6, 7),
         TFN(3, 5, 7), TFN(3, 6, 7), TFN(3, 6, 7), TFN(3, 6, 9), TFN(3, 6, 9),
         TFN(3, 5, 7), TFN(1, 5, 5), TFN(3, 6, 7)],

        [TFN(5, 7, 9), TFN(1, 1, 3), TFN(5, 7, 9), TFN(3, 6, 9), TFN(3, 7, 7),
         TFN(7, 9, 9), TFN(5, 8, 9), TFN(5, 7, 9), TFN(5, 7, 9), TFN(5, 8, 9),
         TFN(5, 7, 9), TFN(5, 8, 9), TFN(5, 8, 9), TFN(5, 7, 9), TFN(5, 8, 9),
         TFN(5, 8, 9), TFN(5, 7, 9), TFN(5, 7, 9)],
    ]

    return X


def load_criteria_dic():
    criteria = {
        "C1": "Product quality/performance",
        "C2": "Rejection rate",
        "C3": "Quality certificate",
        "C4": "Suitable product characteristics",
        "C5": "Product price",
        "C6": "Performance history/History",
        "C7": "Reliability",
        "C8": "React quickly",
        "C9": "Handling and availability support by technical experts",
        "C10": "Compliance standard 0.02",
        "C11": "Proper record on complaints and follow up",
        "C12": "Provide sample before first ordering",
        "C13": "Guarantee & Warranty (GW)",
        "C14": "Service rate",
        "C15": "Training",
        "C16": "Quantity discount is offered by each supplier",
        "C17": "On time delivery",
        "C18": "Products delivered in good condition",

    }

    return criteria


def load_causal_relations():
    edges = [

        ("C3", "C1", 1),
        ("C3", "C2", -1),
        ("C1", "C2", -1),
        ("C4", "C1", 1),
        ("C4", "C2", -1),
        ("C1", "C18", 1),

        ("C6", "C7", 1),
        ("C7", "C17", 1),
        ("C6", "C17", 1),
        ("C7", "C18", 1),

        ("C8", "C11", 1),
        ("C9", "C11", 1),
        ("C14", "C8", 1),

        ("C15", "C2", -1),


        ("C10", "C3", 1),
        ("C12", "C1", 1),
        ("C12", "C2", -1),
        ("C13", "C7", 1),

        ("C5", "C1", -1),
        ("C5", "C7", -1),
        ("C16", "C5", -1),

        ("C17", "C18", 1),
        ("C7", "C8", 1),
        ("C9", "C8", 1),

        ("C11", "C7", 1),
        ("C11", "C6", 1),

        ("C17", "C7", 1),
        ("C14", "C7", 1),

        ("C4", "C18", 1),
        ("C1", "C7", 1)

    ]

    return edges


def load_benefit_cost_vector():
    benefit = [
        1,  # C1
        0,  # C2
        1,  # C3
        1,  # C4
        0,  # C5
        1,  # C6
        1,  # C7
        1,  # C8
        1,  # C9
        1,  # C10
        1,  # C11
        1,  # C12
        1,  # C13
        1,  # C14
        1,  # C15
        1,  # C16
        1,  # C17
        1  # C18
    ]
    return benefit


def load_importance_ranking():
    importance = [
        2,  # C1
        11,  # C2
        7,  # C3
        3,  # C4
        1,  # C5
        6,  # C6
        4,  # C7
        9,  # C8
        5,  # C9
        12,  # C10
        13,  # C11
        8,  # C12
        14,  # C13
        16,  # C14
        17,  # C15
        10,  # C16
        15,  # C17
        18  # C18
    ]
    return importance


def load_roc_weights():
    roc_weights = np.array([0.13,0.02,0.05,0.13,0.22,0.06,0.09,0.03,0.08,0.02,0.02,0.04,0.02,0.01,0.01,0.03,0.02,0.01])
    return  roc_weights

def load_initial_criteria_values():
    initial_criteria_values =  np.full(18, 0.5)
    return initial_criteria_values