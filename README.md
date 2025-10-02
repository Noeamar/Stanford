# STABL – Stability-based Feature Selection with Nonlinear Models

## 📌 À propos

**STABL** (Stability-based feature selection with artificial features) est une méthode de sélection de variables conçue pour identifier des ensembles de features stables et interprétables, même dans des environnements bruités ou de haute dimension.  

Historiquement, STABL s’appuyait sur des modèles linéaires (Lasso, ElasticNet, ALasso). Cela permet d’obtenir des sélections très **parcimonieuses et stables**, mais limitées aux signaux linéaires/monotones.  
Ce projet explore l’extension de STABL avec des **modèles non linéaires**, notamment **XGBoost**, afin de capturer des interactions, seuils et saturations souvent présents dans des données biologiques complexes.

---

## ⚙️ Pipeline STABL

Le pipeline général se déroule en deux phases :

### 1. Sélection de variables
- Génération de **N bootstraps** (≈ 50% des échantillons par bootstrap).  
- Entraînement d’un **modèle de base** sur chaque bootstrap.  
- Récupération des importances de chaque feature.  
- Normalisation ou binarisation des importances.  
- Agrégation des scores sur l’ensemble des bootstraps.  
- Seuil basé sur **contrôle FDR** et **stabilité** pour retenir un ensemble final de features.

### 2. Réentraînement
- Sur les features sélectionnées, on ajuste un modèle final (logistique, linéaire ou non-linéaire selon le cas d’usage).

---

## 🚀 Extension : STABL + XGBoost

### Pourquoi XGBoost ?
- Les modèles linéaires sont efficaces sur signaux monotones.  
- De nombreuses données réelles présentent des **interactions (X₁×X₂)**, des **seuils** ou des **saturations**.  
- **XGBoost** comme estimateur de base permet de capturer ces non-linéarités tout en conservant le principe de stabilité de STABL.

### Importances testées
- `weight` (fréquence d’utilisation d’une feature dans les splits)  
- `gain` (réduction moyenne de la perte due à la feature)  
- `total_gain` (somme des gains)  
- `cover` (nombre moyen d’échantillons séparés par la feature)  
- `total_cover` (somme des couvertures)  
- `SHAP` (attribution locale puis importance globale via TreeSHAP)

### Hyperparamètres explorés
- **Base XGB** pour la sélection :  
  - `max_depth ∈ {3, 6, 9}`  
  - `reg_alpha ∈ {0, 0.5, 1, 2, 5}`  
  - `seed=42`, `B=1000 bootstraps`  

- **Réentraînement final** :  
  - `n_estimators ≈ 200–800`  
  - `learning_rate ∈ [0.01, 0.1]`  
  - `subsample ≈ 0.6`  
  - `colsample_bytree ≈ 0.5`

---

## 📊 Résultats (résumé des datasets)

- **Onset of Labor (CyTOF + Protéomics, regression)**  
  - STABL ElasticNet (linéaire) → baseline  
  - STABL XGBoost → amélioration sur signaux complexes  

- **COVID-19 (classification)**  
  - Best STABL Linear : Lasso  
  - STABL XGBoost : AUROC = **0.891** (vs 0.830), AUPRC = **0.82** (vs 0.74)  

- **CFRNA (classification)**  
  - Best Linear : Lasso  
  - STABL XGBoost : AUROC = **0.871**, AUPRC = **0.92**  

- **Biobank SSI (classification)**  
  - Best Linear : Lasso  
  - STABL XGBoost : AUROC = **0.828**, AUPRC = **0.51**  

---

## 📂 Structure du dépôt

Stanford/
├── src/             
│   ├── stabl_linear/   *Implémentations classiques (Lasso, EN, ALasso)*
│   ├── stabl_xgb/      *Implémentations STABL avec XGBoost*
│   └── utils/          *Fonctions de support (normalisation, métriques…)*
├── notebooks/          *Notebooks d’expérimentation et d’analyse*
├── results/            *Résultats : perfs, features sélectionnées, plots*
├── data/               *Jeux de données (non inclus dans le repo public)*
└── README.md



---

## 🔧 Installation

```bash
# 1. Cloner le repo
git clone https://github.com/Noeamar/Stanford.git
cd Stanford

# 2. Créer un environnement Python
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt
