import psycopg2
import redis
from decimal import Decimal
import time

# Connexion à PostgreSQL
pg_conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="postgres",
    dbname="postgres"
)
pg_cursor = pg_conn.cursor()

# Connexion à Redis
redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)

# Fonction pour lire les données de PostgreSQL et les stocker dans Redis
def sync_postgres_to_redis():
    # Lecture des données de la table PostgreSQL
    pg_cursor.execute("SELECT * FROM taux_de_change;")
    rows = pg_cursor.fetchall()

    # Utilisation du pipelining Redis pour une insertion efficace des données
    pipe = redis_client.pipeline()
    for row in rows:
        key = f"taux_de_change:{row[0]}"  # Utilisation de l'ID comme clé
        value = {
            "devise": row[1],
            "taux": float(row[2]) if isinstance(row[2], Decimal) else row[2]  # Conversion en float si Decimal
        }
        pipe.hset(key, mapping=value)  # Utilisation de hset au lieu de hmset
    pipe.execute()
    print("Données synchronisées de PostgreSQL à Redis en utilisant le pipelining.")

def sync_one_to_many():
    # Lecture des données de la table parent (produits)
    pg_cursor.execute("SELECT * FROM produits;")
    produits = pg_cursor.fetchall()

    for produit in produits:
        produit_id = produit[0]
        produit_nom = produit[1]

        # Stockage du produit dans Redis
        redis_client.hset(f"produit:{produit_id}", mapping={"nom": produit_nom})

        # Lecture des variantes associées au produit
        pg_cursor.execute("SELECT * FROM variantes WHERE produit_id = %s;", (produit_id,))
        variantes = pg_cursor.fetchall()

        # Stockage des variantes dans Redis
        for variante in variantes:
            variante_id = variante[0]
            variante_nom = variante[2]
            variante_prix = float(variante[3])
            redis_client.hset(f"variante:{variante_id}", mapping={
                "produit_id": produit_id,
                "nom": variante_nom,
                "prix": variante_prix
            })

        print(f"Produit {produit_nom} et ses variantes synchronisés dans Redis.")

# Exemple d'utilisation
if __name__ == "__main__":
    sync_postgres_to_redis()
    sync_one_to_many()

    # Section de benchmarking
    # Temps de lecture PostgreSQL
    start_pg = time.perf_counter()
    pg_cursor.execute("SELECT * FROM taux_de_change;")
    pg_data = pg_cursor.fetchall()
    end_pg = time.perf_counter()
    print(f"Temps de lecture PostgreSQL : {end_pg - start_pg:.6f} secondes")

    # Temps de lecture Redis
    start_redis = time.perf_counter()
    for row in pg_data:
        redis_client.hgetall(f"taux_de_change:{row[0]}")
    end_redis = time.perf_counter()
    print(f"Temps de lecture Redis : {end_redis - start_redis:.6f} secondes")

# Fermeture des connexions
pg_cursor.close()
pg_conn.close()