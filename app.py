from flask import Flask, request, jsonify
from ia import critique_site_web
from scrapper import scrapping_site
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Cette ligne permet à toutes les origines de faire des requêtes à ton API

# Fonction pour initialiser la base de données
def init_db():
    conn = sqlite3.connect('website_ratings.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS website_reviews (
        id INTEGER PRIMARY KEY,
        Design TEXT,
        Navigation TEXT,
        Contenu TEXT,
        Services TEXT,
        Contact TEXT,
        Ergonomie TEXT,
        Originalité TEXT,
        Performances TEXT,
        Accessibilite TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Appel de la fonction pour initialiser la base de données
init_db()

@app.route('/flask-function', methods=['GET'])
def flask_function():
    url = request.args.get('url')
    print("nouvelle requête avec l'url", url)

    texts = scrapping_site(url)
    print("Textes scrappés sur l'url", url)
    # Store the result in a variable "scrapping"
    scrapping = ""
    for i, text in enumerate(texts):
        scrapping += f"Texte de la page {i+1}: {text.strip()}\n"
    
    # Exemple d'utilisation
    theme_a_aborder = [
        "Design",
        "Navigation",
        "Contenu",
        "Services",
        "Contact",
        "Ergonomie",
        "Originalité",
        "Performances",
        "Accessibilite",
    ]


    data = {}
    for theme in theme_a_aborder:
        print(f"Theme en cours: {theme}")
        response = critique_site_web(theme, scrapping)
        data[theme.capitalize()] = response


    # Insertion des données dans la base de données et récupération de l'ID
    print("Insertion des données dans la base de données")
    conn = sqlite3.connect('website_ratings.db')
    c = conn.cursor()
    c.execute('''
    INSERT INTO website_reviews (Design, Navigation, Contenu, Services, Contact, Ergonomie, Originalité, Performances, Accessibilite)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data.get('Design'), data.get('Navigation'), data.get('Contenu'), data.get('Services'), data.get('Contact'), data.get('Ergonomie'), data.get('Originalité'), data.get('Performances'), data.get('Accessibilite')))
    review_id = c.lastrowid
    conn.commit()
    conn.close()
    
    print("ID:", review_id)
    return jsonify({"id": review_id})

@app.route('/api/data/<int:id>', methods=['GET'])
def get_data_by_id(id):
    conn = sqlite3.connect('website_ratings.db')
    c = conn.cursor()
    c.execute('SELECT * FROM website_reviews WHERE id = ?', (id,))
    row = c.fetchone()
    conn.close()

    if row:
        data = {
            "id": row[0],
            "Design": row[1],
            "Navigation": row[2],
            "Contenu": row[3],
            "Services": row[4],
            "Contact": row[5],
            "Ergonomie": row[6],
            "Originalité": row[7],
            "Performances": row[8],
            "Accessibilite": row[9]
        }
        print(row[9])
        return jsonify(data)
    else:
        return jsonify({"error": "ID not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
