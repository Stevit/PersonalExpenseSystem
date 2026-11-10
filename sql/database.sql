CREATE TABLE IF NOT EXISTS categorie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE CHECK (length(nome) > 0)
);

CREATE TABLE IF NOT EXISTS spese (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL CHECK (length(data) = 10),
    importo REAL NOT NULL CHECK (importo > 0),
    categoria_id INTEGER NOT NULL,
    descrizione TEXT,
    FOREIGN KEY (categoria_id) REFERENCES categorie(id)
);

CREATE TABLE IF NOT EXISTS budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mese TEXT NOT NULL CHECK (length(mese) = 7),
    categoria_id INTEGER NOT NULL,
    importo REAL NOT NULL CHECK (importo > 0),
    UNIQUE (mese, categoria_id),
    FOREIGN KEY (categoria_id) REFERENCES categorie(id)
);

INSERT INTO categorie (id, nome) VALUES (1, 'Alimentari');
INSERT INTO categorie (id, nome) VALUES (2, 'Trasporti');
INSERT INTO categorie (id, nome) VALUES (3, 'Svago');

INSERT INTO budget (id, mese, categoria_id, importo) VALUES (1, '2025-01', 1, 300.00);
INSERT INTO budget (id, mese, categoria_id, importo) VALUES (2, '2025-01', 2, 150.00);

INSERT INTO spese (id, data, importo, categoria_id, descrizione) VALUES (1, '2025-01-10', 295.50, 1, 'Spesa supermercato');
INSERT INTO spese (id, data, importo, categoria_id, descrizione) VALUES (2, '2025-01-15', 25.00, 1, 'Pranzo');
INSERT INTO spese (id, data, importo, categoria_id, descrizione) VALUES (3, '2025-01-18', 120.00, 2, 'Abbonamento mezzi');

