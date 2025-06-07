from flask import Flask, request, jsonify
import sqlite3
from nlp.query_handler import ask_question


app = Flask(__name__)

@app.route('/produits', methods=['GET'])
def get_produits():
    conn = sqlite3.connect("./dat/database.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produits ORDER BY ca DESC')
    produits = cursor.fetchall()
    conn.close()
    produits = [
        {
            "id": row[0],
            "nom": row[1],
            "categorie": row[2],
            "mois": row[3],
            "marge": row[4],
            "ca": row[5],
            "fournisseur": row[6]
        } for row in produits
    ]
       
    return jsonify(produits)    



@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return {"error": "Aucune question fournie"}, 400

    answer = ask_question(question)
    
    
    return {"question": question, "answer": answer}


if __name__ == "__main__":
    app.run(debug=True)