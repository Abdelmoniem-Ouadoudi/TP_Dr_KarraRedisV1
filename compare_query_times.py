import time
import psycopg2
import redis

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

# Fonction pour mesurer le temps de requêtage dans PostgreSQL
def query_postgres():
    start_time = time.time()
    pg_cursor.execute("SELECT * FROM taux_de_change;")
    rows = pg_cursor.fetchall()
    end_time = time.time()
    print(f"PostgreSQL - Temps de requêtage : {end_time - start_time:.6f} secondes")
    return rows

# Fonction pour mesurer le temps de requêtage dans Redis
def query_redis():
    start_time = time.time()
    keys = redis_client.keys("taux_de_change:*")
    rows = [redis_client.hgetall(key) for key in keys]
    end_time = time.time()
    print(f"Redis - Temps de requêtage : {end_time - start_time:.6f} secondes")
    return rows

# Fonction pour mesurer le temps de requêtage pour une relation one-to-many dans PostgreSQL
def query_postgres_one_to_many():
    start_time = time.time()
    pg_cursor.execute("""
        SELECT p.nom AS produit, v.nom AS variante, v.prix
        FROM produits p
        JOIN variantes v ON p.id = v.produit_id;
    """)
    rows = pg_cursor.fetchall()
    end_time = time.time()
    print(f"PostgreSQL (one-to-many) - Temps de requêtage : {end_time - start_time:.6f} secondes")
    return rows

# Fonction pour mesurer le temps de requêtage pour une relation one-to-many dans Redis
def query_redis_one_to_many():
    start_time = time.time()
    produits = redis_client.keys("produit:*")
    result = []

    for produit_key in produits:
        produit_id = produit_key.split(":")[1]
        produit_nom = redis_client.hget(produit_key, "nom")

        variantes = redis_client.keys(f"variante:*")
        for variante_key in variantes:
            variante_data = redis_client.hgetall(variante_key)
            if variante_data["produit_id"] == produit_id:
                result.append({
                    "produit": produit_nom,
                    "variante": variante_data["nom"],
                    "prix": variante_data["prix"]
                })

    end_time = time.time()
    print(f"Redis (one-to-many) - Temps de requêtage : {end_time - start_time:.6f} secondes")
    return result

# Exemple d'utilisation
if __name__ == "__main__":
    print("Requêtage dans PostgreSQL :")
    postgres_data = query_postgres()
    print(postgres_data)

    print("\nRequêtage dans Redis :")
    redis_data = query_redis()
    print(redis_data)

    print("Requêtage one-to-many dans PostgreSQL :")
    postgres_data = query_postgres_one_to_many()
    print(postgres_data)

    print("\nRequêtage one-to-many dans Redis :")
    redis_data = query_redis_one_to_many()
    print(redis_data)

# Fermeture des connexions
pg_cursor.close()
pg_conn.close()