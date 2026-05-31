import duckdb

db_path = "ventes.duckdb"

# Définition des colonnes attendues
required_columns = {"date", "produit", "categorie", "quantite", "prix_unitaire", "ville"}

# Connexion à la base DuckDB
con = duckdb.connect(db_path)

# 1. Vérification des colonnes existantes
columns = con.execute("DESCRIBE ventes_raw").fetchall()
existing_columns = {col[0] for col in columns}

missing = required_columns - existing_columns
if missing:
    con.close()
    raise ValueError(f"Colonnes manquantes: {missing}")

# 2. Vérification des valeurs NULL sur les colonnes critiques
null_count = con.execute("""
    SELECT COUNT(*) FROM ventes_raw
    WHERE produit IS NULL OR quantite IS NULL OR prix_unitaire IS NULL
""").fetchone()[0]

con.close()

if null_count > 0:
    raise ValueError(f"Données invalides : {null_count} lignes incomplètes.")
else:
    print("Validation réussie : schéma et qualité minimale OK")
