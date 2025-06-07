# chatbot-analytics

Assistant produit en langage naturel permettant d'interroger une base de données sur les ventes (CA, marge, fournisseur…) via une interface Streamlit et un backend Flask connecté à l'API Hugging Face.

### Prérequis
Python 3.9+
Git
Token Hugging Face

### 1. Installation
Cloner le projet
git clone https://github.com/Khalilz00/chatbot-analytics.git
cd chatbot-analytics

### 2. Créer un environnement virtuel

#### Windows :
python -m venv venv
venv\Scripts\activate

#### macOS/Linux :
python3 -m venv venv
source venv/bin/activate

### 3. Installer les dépendances
pip install -r backend/requirements.txt

### 4. Créer la base de données
python backend/db_init.py

### 5. Configuration du token Hugging Face
Créer un fichier .env à la racine du projet.

### 6. Ajouter votre token Hugging Face :

HF_TOKEN="Bearer votre_token_personnel_ici"


### 7. Lancement du projet
Lancer le backend Flask (dans un terminal)
python backend/app.py

### 8. Lancer le frontend Streamlit (dans un autre terminal, avec le même venv activé)
streamlit run frontend/streamlit_app.py

### 9. Utilisation
Entrez une question dans l’interface (ex. : Quel est le plus haut chiffre d'affaire ?)

Le backend transforme cette question en requête SQL grâce à l’API Hugging Face.

Les résultats sont affichés dans Streamlit.

### Structure du projet
backend/ : API Flask + logique NLP

frontend/ : Interface utilisateur Streamlit

data/ : Base de données SQLite

.env : Token Hugging Face (non versionné)
