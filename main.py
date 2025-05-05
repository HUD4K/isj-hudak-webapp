# Je NUTNÉ nainštalovať alíček: do konzoly napíšte "pip install flask"
from flask import Flask, request, render_template
import sqlite3
import hashlib

app = Flask(__name__)


# rýchly úvod do HTML elementov:
# <h1> ...text... </h1>, alebo <h2>             - heading - nadpisy
# <p> ...text... </p>                           - paragraf (normálny text)
# <a href="www.---.com"> ...text...></a>        - odkaz (v rámci textu)
# <button> ...text... </button>                 - tlačidlo s textom
# <hr>                                          - čiara

# Pripojenie k databáze
def pripoj_db():
    conn = sqlite3.connect("kurzy.db")
    return conn


@app.route('/')  # API endpoint
def index():
    # Úvodná homepage s dvoma tlačidami ako ODKAZMI na svoje stránky - volanie API nedpointu
    return '''
        <h1>Výber z databázy</h1>
        <a href="/kurzy"><button>Zobraz všetky kurzy</button></a>
        <a href="/treneri"><button>Zobraz všetkých trénerov</button></a>
        <a href="/registracia"><button>Registruj trénera</button></a>
        <hr>
    '''


@app.route('/kurzy')
def zobraz_kurzy():
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Kurzy")
    kurzy = cursor.fetchall()
    conn.close()

    return render_template("kurzy.html", kurzy=kurzy)


# PODSTRÁNKA NA ZOBRAZENIE TRÉNEROV
@app.route('/treneri')  # API endpoint
def zobraz_trenerov():
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT T.ID_trenera, T.Meno || ' ' || T.Priezvisko as Trener, Nazov_kurzu
        FROM Treneri T LEFT JOIN Kurzy K ON T.ID_trenera = K.ID_trenera
    """)
    treneri = cursor.fetchall()

    conn.close()

    # Jednoduchý textový výpis trénerov a ich kurzov
    vystup = "<h2>Zoznam trénerov a kurzov:</h2>"
    for trener in treneri:
        vystup += f"<p>{trener}</p>"

    # Odkaz na návrat
    vystup += '<a href="/">Späť</a>'
    return vystup

# Metóda je GET. (Predtým sme metódu nedefinovali. Ak žiadnu neuvedieme, automaticky je aj tak GET)
@app.route('/registracia', methods=['GET'])
def registracia_form():
    return '''
        <h2>Registrácia trénera</h2>
        <form action="/registracia" method="post">
            <label>Meno:</label><br>
            <input type="text" name="meno" required><br><br>

            <label>Priezvisko:</label><br>
            <input type="text" name="priezvisko" required><br><br>

            <label>Špecializácia:</label><br>
            <input type="text" name="specializacia" required><br><br>

            <label>Telefón:</label><br>
            <input type="text" name="telefon" required><br><br>

            <label>Heslo:</label><br>
            <input type="password" name="heslo" required><br><br>

            <button type="submit">Registrovať</button>
        </form>
        <hr>
        <a href="/">Späť</a>
    '''


# API ENDPOINT NA SPRACOVANIE REGISTRÁCIE. Mapuje sa na mená elementov z formulára z predošlého requestu (pomocou request.form[...])
# Pozor - metóda je POST
@app.route('/registracia', methods=['POST'])
def registracia_trenera():
    meno = request.form['meno']
    priezvisko = request.form['priezvisko']
    specializacia = request.form['specializacia']
    telefon = request.form['telefon']
    heslo = request.form['heslo']

    # Hashovanie hesla
    heslo_hash = hashlib.sha256(heslo.encode()).hexdigest()

    # Zápis do databázy
    conn = pripoj_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Treneri (Meno, Priezvisko, Specializacia, Telefon, Heslo) VALUES (?, ?, ?, ?, ?)", 
                   (meno, priezvisko, specializacia, telefon, heslo_hash))
    conn.commit()
    conn.close()

    # Hlásenie o úspešnej registrácii
    return '''
        <h2>Tréner bol úspešne zaregistrovaný!</h2>
        <hr>
        <a href="/">Späť</a>
    '''


if __name__ == '__main__':
    app.run(debug=True)


# Aplikáciu spustíte, keď do konzoly napíšete "python app.py"