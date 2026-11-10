import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spese.db")

def init_db(conn):
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categorie (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE CHECK (length(nome) > 0)
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS spese (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL CHECK (length(data) = 10),
        importo REAL NOT NULL CHECK (importo > 0),
        categoria_id INTEGER NOT NULL,
        descrizione TEXT,
        FOREIGN KEY (categoria_id) REFERENCES categorie(id)
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS budget (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mese TEXT NOT NULL CHECK (length(mese) = 7),
        categoria_id INTEGER NOT NULL,
        importo REAL NOT NULL CHECK (importo > 0),
        UNIQUE (mese, categoria_id),
        FOREIGN KEY (categoria_id) REFERENCES categorie(id)
    );
    """)
    conn.commit()

def gestione_categorie(conn):
    nome = input("Inserisci il nome della categoria: ").strip()
    if not nome:
        print("Errore: il nome della categoria non puo essere vuoto.")
        return
    cur = conn.cursor()
    cur.execute("SELECT id FROM categorie WHERE nome = ?", (nome,))
    if cur.fetchone():
        print("La categoria esiste già.")
        return
    cur.execute("INSERT INTO categorie (nome) VALUES (?)", (nome,))
    conn.commit()
    print("Categoria inserita correttamente.")

def inserisci_spesa(conn):
    data = input("Data (formato YYYY-MM-DD): ").strip()
    try:
        importo = float(input("Importo: ").strip())
    except ValueError:
        print("Errore: l'importo deve essere maggiore di zero.")
        return
    if importo <= 0:
        print("Errore: l'importo deve essere maggiore di zero.")
        return
    categoria = input("Nome della categoria: ").strip()
    descrizione = input("Descrizione facoltativa: ").strip()
    cur = conn.cursor()
    cur.execute("SELECT id FROM categorie WHERE nome = ?", (categoria,))
    row = cur.fetchone()
    if not row:
        print("Errore: la categoria non esiste.")
        return
    cur.execute("INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES (?, ?, ?, ?)", (data, importo, row[0], descrizione))
    conn.commit()
    print("Spesa inserita correttamente.")

def definisci_budget(conn):
    mese = input("Mese (YYYY-MM): ").strip()
    categoria = input("Nome della categoria: ").strip()
    try:
        importo = float(input("Importo del budget: ").strip())
    except ValueError:
        print("Errore: l'importo deve essere maggiore di zero.")
        return
    if importo <= 0:
        print("Errore: l'importo deve essere maggiore di zero.")
        return
    cur = conn.cursor()
    cur.execute("SELECT id FROM categorie WHERE nome = ?", (categoria,))
    row = cur.fetchone()
    if not row:
        print("Errore: la categoria non esiste.")
        return
    cur.execute("INSERT INTO budget (mese, categoria_id, importo) VALUES (?, ?, ?) ON CONFLICT(mese, categoria_id) DO UPDATE SET importo = excluded.importo", (mese, row[0], importo))
    conn.commit()
    print("Budget mensile salvato correttamente.")

def report_totale_per_categoria(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT c.nome, COALESCE(SUM(s.importo), 0.0)
        FROM categorie c
        JOIN spese s ON c.id = s.categoria_id
        GROUP BY c.id, c.nome
    """)
    rows = cur.fetchall()
    print(f"{'Categoria':.<17}Totale Speso")
    for row in rows:
        print(f"{row[0]:.<17}{row[1]:.2f}")

def report_spese_vs_budget(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT b.mese, c.nome, b.importo, COALESCE(SUM(s.importo), 0.0)
        FROM budget b
        JOIN categorie c ON b.categoria_id = c.id
        LEFT JOIN spese s ON s.categoria_id = c.id AND substr(s.data, 1, 7) = b.mese
        GROUP BY b.id, b.mese, c.nome, b.importo
    """)
    rows = cur.fetchall()
    for mese, cat, b_val, speso in rows:
        if speso > b_val:
            stato = "SUPERAMENTO BUDGET"
        else:
            stato = "OK"
        print(f"Mese: {mese}")
        print(f"Categoria: {cat}")
        print(f"Budget: {b_val:g}")
        print(f"Speso: {speso:g}")
        print(f"Stato: {stato}")
        print()

def report_elenco_spese(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT s.data, c.nome, s.importo, COALESCE(s.descrizione, '')
        FROM spese s
        JOIN categorie c ON s.categoria_id = c.id
        ORDER BY s.data ASC
    """)
    rows = cur.fetchall()
    print(f"{'Data':<12}{'Categoria':<15}{'Importo':<10}{'Descrizione'}")
    print("-" * 62)
    for row in rows:
        print(f"{row[0]:<12}{row[1]:<15}{row[2]:<10.2f}{row[3]}")

def menu_report(conn):
    while True:
        print("-------------------------")
        print("MENU DEI REPORT")
        print("-------------------------")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese ordinate per data")
        print("4. Ritorna al menu principale")
        print("-------------------------")
        scelta = input("Inserisci la tua scelta: ").strip()
        match scelta:
            case "1":
                report_totale_per_categoria(conn)
            case "2":
                report_spese_vs_budget(conn)
            case "3":
                report_elenco_spese(conn)
            case "4":
                break
            case _:
                print("Scelta non valida. Riprovare.")

def main():
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    print("Benvenuto nel Sistema di Gestione delle Spese Personali e del Budget")
    while True:
        print("-------------------------")
        print("SISTEMA SPESE PERSONALI")
        print("-------------------------")
        print("1. Gestione Categorie")
        print("2. Inserisci Spesa")
        print("3. Definisci Budget Mensile")
        print("4. Visualizza Report")
        print("5. Esci")
        print("-------------------------")
        scelta = input("Inserisci la tua scelta: ").strip()
        match scelta:
            case "1":
                gestione_categorie(conn)
            case "2":
                inserisci_spesa(conn)
            case "3":
                definisci_budget(conn)
            case "4":
                menu_report(conn)
            case "5":
                break
            case _:
                print("Scelta non valida. Riprovare.")
    conn.close()

if __name__ == "__main__":
    main()

