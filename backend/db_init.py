import sqlite3
from faker import Faker
import random

def create_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Crée une table Produits
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            categorie TEXT,
            mois TEXT,
            marge FLOAT,
            ca INTEGER,
            fournisseur TEXT
        )
    ''')

    # Simuler des données
    fake = Faker("fr_FR")
    fournisseurs = ["Nike", "Adidas", "Puma", "Reebok", "Asics"]
    categories = ["Chaussures", "Textile", "Accessoires"]

    for _ in range(30):
        cursor.execute('''
            INSERT INTO produits (nom, categorie, mois, marge, ca, fournisseur)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            fake.word().capitalize(),
            random.choice(categories),
            "2025-05",
            round(random.uniform(5, 40), 2),
            random.randint(1000, 10000),
            random.choice(fournisseurs)
        ))

    conn.commit()
    conn.close()
    print("Base de données créée avec succès.")

if __name__ == "__main__":
    create_db()
