# Supplier Selection Decision Support Framework

Framework sperimentale per la **selezione dei fornitori** nell'ambito del procurement aziendale basato sull’integrazione di:

- Fuzzy Cognitive Maps (FCM)
- Particle Swarm Optimization (PSO)
- Fuzzy TOPSIS: Metodo di Multi-Criteria Decision Making 

Questo progetto è stato sviluppato come supporto per la mia tesi di laurea triennale in Informatica all'università di Bari Aldo Moro.

Tesi di laurea in: Computational Intelligence

Relatore: Prof. Corrado Mencar

Correlatore: Dr. Davide Cazzorla


In questo lavoro si propone una metodologia innovativa per affrontare il problema della supplier selection in modo più approfondito rispetto agli approcci tradizionali della letteratura, 
i quali considerano i criteri come statici ed indipendenti mentre in questo lavoro si introduce la dinamicità dei criteri considerando come interagiscono fra loro (Fuzzy Cognitive Map).

---

## 🎯 Obiettivo

L’obiettivo del framework è:

- modellare le **relazioni causali** tra i criteri di valutazione, rappresentandoli attraverso un grafo;
- ottimizzare tali relazioni tramite PSO, sulla base di una **funzione di fitness**;
- trasformare la struttura causale in un **vettore dei pesi** che stabilisce l'importanza dei criteri, attraverso tecniche di trasformazione;
- utilizzare i pesi nel **Fuzzy TOPSIS** per ottenere il ranking finale dei fornitori.
- confrontare i risultati raggiunti (ranking dei fornitori, vettori d'importanza) fra gli approcci della metodologia e l'articolo di riferimento

---

## 🧠 Metodologia

Il workflow del framework è il seguente:

1. Definizione dei criteri di valutazione
2. Costruzione della Fuzzy Cognitive Map iniziale
3. Inizializzazione della matrice dei pesi \( W_0 \)
4. Ottimizzazione della matrice tramite PSO + FCM reasoning
5. Ottenimento della matrice ottimizzata \( W_{best} \)
6. Trasformazione della matrice in un vettore dei pesi
7. Applicazione del Fuzzy TOPSIS
8. Ranking finale dei fornitori in base al coefficiente di vicinanza relativa (Relative Closeness)

---

## ⚙️ Struttura del progetto

- `classes.py`  
  Contiene le classi principali (es. TFN, Selector)

- `dataset.py`  
  Gestione del dataset e dei criteri

- `graph.py`  
  Costruzione e visualizzazione della FCM

- `pso_fcm_reasoning.py`  
  Reasoning FCM, funzione di fitness e PSO

- `weights_transformation.py`  
  Trasformazione dei pesi:
  - ROC-based
  - Centrality-based
  - Matrice d' importanza

- `fuzzy_topsis.py`  
  Implementazione del metodo Fuzzy TOPSIS

- `main.py`  
  Esecuzione dell’intero workflow

---

## 🔄 Trasformazione dei pesi

Il framework implementa due approcci:

### 1. ROC-based
Basato su Rank Order Centroid (richiede un ranking iniziale d'importanza dei criteri)

### 2. Centrality-based
Basato su **Eigenvector Centrality** applicato al grafo inverso della FCM

👉 Vantaggio:
- non richiede input degli esperti
- risultati nel dataset selezionato quasi identici al ROC a livello di RC

---

## 📊 Dataset

Caso studio basato su un problema di supplier selection per apparecchiature medicali.

Sono utilizzati:
- 18 criteri
- vettore ROC
- fuzzy decision matrix

Definiti nella tesi:
- classificazione benefit/cost
- relazioni causali tra criteri
- valori iniziali per il reasoning dei criteri

---

## ▶️ Esecuzione

Per eseguire il progetto:

```bash
python main.py

## 📈 Output

Il framework produce:

- matrice iniziale W0
- matrice ottimizzata W_best
- vettore dei pesi dei criteri
- ranking finale dei fornitori


---

## 📌 Risultati principali

- Il framework produce un ranking **chiaro e ben discriminante** nei valori di RC
- Le trasformazioni **ROC-based** e **centrality-based** generano risultati molto simili
- La trasformazione **centrality-based** non richiede un ranking iniziale dei criteri, risulta più efficace

---

## 🚀 Sviluppi futuri

- validazione con esperti di dominio
- applicazione ad altri dataset
- sperimentazione di altri approcci di MCDM
- sperimentazione di altre metriche di centralità
