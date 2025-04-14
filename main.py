from flask import Flask,  redirect, url_for,request
import sqlite3
import hashlib

app = Flask(__name__)


# rýchly úvod do HTML elementov:
# <h1> ...text... </h1>, alebo <h2>             - heading - nadpisy
# <p> ...text... </p>                           - paragraf (normálny text)
# <a href="www.---.com"> ...text...></a>        - odkaz (v rámci textu)
# <button> ...text... </button>                 - tlačidlo s textom


# Pripojenie k databáze
def pripoj_db():
    try:
        conn = sqlite3.connect("kurzy.db")
        return conn
    except sqlite3.Error:
        return None  # Ak sa nepodarí pripojiť, vráti None


@app.route('/')  # API endpoint
def index():
    # Úvodná homepage s dvoma tlačidami ako ODKAZMI na svoje stránky - volanie API nedpointu
    return '''
        <h1>Výber z databázy</h1>
        <ul class="navbar">
        <li><a href="/registracia">1 - Registrácia nového trénera</a></li>
        <li><a href="/treneri_a_kurz">2 - Výpis všetkých trénerov a ich kurzov</a></li>
        <li><a href="/kurzy">3 - Výpis všetkých kurzov</a></li>
        <li><a href="/miesta">4 - Výpis všetkých miest </a></li>
        <li><a href="/capacita">5 - Výpis súčtu maximálnej kapacity všetkých kurzov na P</a></li>
        </ul>
        

        <style>
        .navbar{
        list-style-type: none;
        

        }
        h1{
        font-family: "Afacad Flux", sans-serif;
        font-weight:700;
        font-size:200px;
        }
        .navbar li{
        margin: 0 5 8 0;
        display: inline;
        float: left;
        padding:15px;
        background-color: #04AA6D;
        }
        a{
        text-decoration:none;
        display: block;
        padding: 5px;
        color:black;
        font-family: "Afacad Flux", sans-serif;
        font-weight:600;
        }
        li:hover {
            background-color:rgb(2, 118, 75);
        }

        </style>
    '''


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



@app.route('/kurzy')  
def zobraz_kurzy():
    conn = pripoj_db()
    if conn is None:
        return redirect(url_for('zobraz_error'))  # Ak DB nefunguje, presmeruje na 404
    
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Kurzy")
    kurzy = cursor.fetchall()

    conn.close()

    # Hlavička tabuľky (prispôsob podľa štruktúry tabuľky v DB)
    vystup = """
    <h2>Zoznam kurzov:</h2>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Názov kurzu</th>
            
        </tr>


    <style>
     table {
        width: 80%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
        font-family: "Afacad Flux", sans-serif;
        font-weight:450;
    }
    th, td {
        padding: 12px;
        border: 1px solid black;
        
    }
    th {
        background-color:  #04AA6D;
    }

    button {
        border: none;
        background-color: white;
        color:black;
        padding: 16px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border: 2px solid #04AA6D;
        font-family: "Afacad Flux", sans-serif;
        font-weight:600;
        
}


button:hover {
  background-color: #04AA6D;
  color: white;
}
</style>
    """

    # Naplnenie tabuľky dátami
    for kurz in kurzy:
        vystup += f"<tr><td>{kurz[0]}</td><td>{kurz[1]}</td></tr>"

    vystup += "</table>"  # Uzavrieme tabuľku
    vystup += '<br><a href="/"><button>Späť</button></a>'  # Tlačidlo na návrat
    return vystup




@app.route('/miesta')  
def zobraz_miesta():
    conn = pripoj_db()
    if conn is None:
        return redirect(url_for('zobraz_error'))  # Ak DB nefunguje, presmeruje na 404
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Miesta")
    miesta = cursor.fetchall()

    conn.close()

    vystup = """
    <h2>Zoznam miest:</h2>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Názov miesta</th>
            <th>Adresa</th>
        </tr>

         <style>
    table {
        width: 80%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
        font-family: "Afacad Flux", sans-serif;
        font-weight:450;
    }
    th, td {
        padding: 12px;
        border: 1px solid black;
    }
    th {
        background-color:  #04AA6D;
    }

    button {
        border: none;
        background-color: white;
        color:black;
        padding: 16px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border: 2px solid #04AA6D;
        font-family: "Afacad Flux", sans-serif;
        font-weight:600;
}


button:hover {
  background-color: #04AA6D;
  color: white;
  font-family: "Afacad Flux", sans-serif;
  font-weight:600;
}
</style>
    """

    for miesto in miesta:
        vystup += f"<tr><td>{miesto[0]}</td><td>{miesto[1]}</td><td>{miesto[2]}</td></tr>"

    vystup += "</table>"
    vystup += '<br><a href="/"><button>Späť</button></a>'
    return vystup



# PODSTRÁNKA NA ZOBRAZENIE TRÉNEROV
@app.route('/treneri_a_kurz')  # API endpoint
def zobraz_trenerov_kurz():
    conn = pripoj_db()
    if conn is None:
        return redirect(url_for('zobraz_error'))  # Ak DB nefunguje, presmeruje na 404
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM VSETCI_TRENERI_A_ICH_KURZY")
    kurzy = cursor.fetchall()

    conn.close()

    # Hlavička tabuľky (prispôsob podľa štruktúry tabuľky v DB)
    vystup = """
    <h2>Zoznam kurzov:</h2>
    <table border="1">
        <tr>
            <th>ID Trenera</th>
            <th>Meno Trenera</th>
            <th>Názov kurzu</th>
        </tr>


         <style>
    table {
        width: 80%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
        font-family: "Afacad Flux", sans-serif;
        font-weight:450;
    }
    th, td {
        padding: 12px;
        border: 1px solid black;
    }
    th {
        background-color:  #04AA6D;
    }

    button {
        border: none;
        background-color: white;
        color:black;
        padding: 16px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border: 2px solid #04AA6D;
        font-family: "Afacad Flux", sans-serif;
        font-weight:600;
}


button:hover {
  background-color: #04AA6D;
  color: white;
  font-family: "Afacad Flux", sans-serif;
  font-weight:600;
}
</style>
    """

    # Naplnenie tabuľky dátami
    for trener in kurzy:
        vystup += f"<tr><td>{trener[0]}</td><td>{trener[1]}</td><td>{trener[2]}</td></tr>"

    vystup += "</table>"  # Uzavrieme tabuľku
    vystup += '<br><a href="/"><button>Späť</button></a>'  # Tlačidlo na návrat
    return vystup


@app.route('/capacita')  # API endpoint
def zobraz_capacitu():
    conn = pripoj_db()
    if conn is None:
        return redirect(url_for('zobraz_error'))  # Ak DB nefunguje, presmeruje na 404
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(Max_pocet_ucastnikov) FROM Kurzy WHERE Nazov_kurzu LIKE 'P%'")
    capacita = cursor.fetchall()

    conn.close()

    # Hlavička tabuľky (prispôsob podľa štruktúry tabuľky v DB)
    vystup = """
    <h2>Zoznam kurzov:</h2>
    <table border="1">
        <tr>
            <th>Suma</th>
            
        </tr>


        <style>
    table {
        width: 80%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
        font-family: "Afacad Flux", sans-serif;
        font-weight:450;
    }
    th, td {
        padding: 12px;
        border: 1px solid black;
    }
    th {
        background-color:  #04AA6D;
    }

    button {
        border: none;
        background-color: white;
        color:black;
        padding: 16px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border: 2px solid #04AA6D;
        font-family: "Afacad Flux", sans-serif;
        font-weight:600;
}


button:hover {
  background-color: #04AA6D;
  color: white;
}
</style>
    """

    # Naplnenie tabuľky dátami
    for cap in capacita:
        vystup += f"<tr><td>{cap[0]}</td></tr>"

    vystup += "</table>"  # Uzavrieme tabuľku
    vystup += '<br><a href="/"><button>Späť</button></a>'  # Tlačidlo na návrat
    return vystup


@app.route('/404')
def zobraz_error():
    return '''
    <h1>ERROR 404 :(</h1>
    <p>Požadovaná stránka neexistuje alebo sa vyskytla chyba pri načítaní databázy.</p>
    <br><a href="/"><button>Späť</button></a>
    <style>
        h1 { color: red; }
        button {
            border: none;
            background-color: white;
            color: black;
            padding: 16px 32px;
            font-size: 16px;
            border: 2px solid #04AA6D;
            cursor: pointer;
            font-family: "Afacad Flux", sans-serif;
            font-weight:450;
        }
        button:hover {
            background-color: #04AA6D;
            color: white;
            font-family: "Afacad Flux", sans-serif;
            font-weight:450;
        }
    </style>
    '''
    vystup += '<br><a href="/"><button>Späť</button></a>'  
    return vystup


if __name__ == '__main__':
    app.run(debug=True)


# Aplikáciu spustíte, keď do konzoly napíšete "python app.py"