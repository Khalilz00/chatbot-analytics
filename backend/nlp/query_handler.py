import sqlite3
import requests
import os
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HUGGINGFACE_API_TOKEN = os.getenv("HF_TOKEN")

headers = {
    "Authorization": HUGGINGFACE_API_TOKEN
}



def generate_sql_from_question(question):
    # Schéma de la base (doit être à jour si tu changes la BDD)
    schema = """
Tu interagis avec une base de données SQLite contenant une table appelée `produits` avec les colonnes suivantes :

- id (entier)
- nom (texte) → nom du produit
- categorie (texte)
- mois (texte, format AAAA-MM)
- marge (nombre, en %)
- ca (nombre, chiffre d'affaires)
- fournisseur (texte)
"""

    prompt = f"""{schema}

Formule une requête SQL (SQLite) correspondant à la question suivante :

Question : {question}

SQL =>
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.2
        }
    }

    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        text = response.json()[0]["generated_text"]
        # On récupère ce qui suit "SQL =>"
        return text.split("SQL =>")[-1].strip()
    else:
        return f"Erreur : {response.status_code} - {response.text}"    


def clean_sql_query(raw_query: str) -> str:
    # Supprime les backticks et les blocs Markdown éventuels
    cleaned = raw_query.strip().strip("`").strip()
    # Supprime les blocs ```sql``` éventuels
    cleaned = cleaned.replace("```sql", "").replace("```", "")
    return cleaned.strip()


def execute_sql_query(sql_query):
    try: 
        conn = sqlite3.connect("./data/database.db")
        cursor = conn.cursor()
        cursor.execute(clean_sql_query(sql_query))
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        return f"Erreur lors de l'exécution de la requête SQL : {e}"


def format_results(results, question):
    prompt = f"""

Voici la question et les résultats de la requête SQL exécutée :

Question : {question}

Résultats de la requête SQL : {results}

Réponds à la question en te basant sur les résultats fournis. Réponse =>

"""
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.2
        }
    }

    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        text = response.json()[0]["generated_text"]
        # On récupère ce qui suit "Réponse =>"
        return text.split("Réponse =>")[-1].strip()
    else:
        return f"Erreur : {response.status_code} - {response.text}"    

    
def ask_question(question):
    sql_query = generate_sql_from_question(question)
    if "Erreur" in sql_query:
        return sql_query  # Retourne l'erreur si la génération de SQL a échoué

    results = execute_sql_query(sql_query)
    if "Erreur" in results:
        return results  # Retourne l'erreur si l'exécution de la requête SQL a échoué

    formatted_results = format_results(results, question)
    return formatted_results
    