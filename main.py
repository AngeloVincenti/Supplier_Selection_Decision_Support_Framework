
from pso_fcm_reasoning import *
from fuzzy_topsis import *
from weights_transformation import *
from graph import *
from dataset import *
from classes import *




# caricamento dataset standard

X = load_fuzzy_decision_matrix()


print("Fuzzy Decision Matrix")
print_fuzzy_matrix(X)
sep()

criteria_set = load_criteria_dic()
benefit = load_benefit_cost_vector()
roc_vector = load_roc_weights()



A0 = load_initial_criteria_values()
causal_relations = load_causal_relations()


#applicazione metodologia

causal_graph = init_graph(criteria_set,causal_relations)

pos = plot_fcm(causal_graph,benefit)

selector_list = extract_range(X)

W0,nodes = initialize_weight_matrix(causal_graph,seed=42) #seed = 42

W_best, fitness_score = pso(W0, A0, selector_list, swarm_size=30, iterations=500, seed=42)


while scelta := int(input("Inserire funzione di trasformazione (1-2-3): ")):

    match scelta:
        case 1:
             pass

        case 2:
             weights_vector = transformation_roc_vector(W_best,roc_vector)

             print("Weights Vector using ROC")
             print(weights_vector)

             sep()

             RC,ranking = fuzzy_topsis(X,weights_vector,benefit)
             print_results(RC,ranking)

        case 3:
            weighted_graph = build_weighted_graph(W_best,nodes)

            plot_fcm(weighted_graph,benefit,edge_type="weights",position = pos)

            abs_weighted_graph = build_weighted_graph(np.abs(W_best),nodes)

            reversed_graph = abs_weighted_graph.reverse()
            plot_fcm(reversed_graph,benefit,edge_type="abs",position = pos)



            weights_vector = transformation_centrality(reversed_graph,nodes)



            RC, ranking = fuzzy_topsis(X, weights_vector, benefit)

            print_results(RC,ranking)





