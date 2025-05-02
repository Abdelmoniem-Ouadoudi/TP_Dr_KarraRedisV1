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

# Fonction pour mesurer le temps de requêtage dans Redis (optimisée avec pipelining)
def query_redis():
    start_time = time.time()
    pg_data = query_postgres()
    pipe = redis_client.pipeline()
    for row in pg_data:
        pipe.hgetall(f"taux_de_change:{row[0]}")
    rows = pipe.execute()
    end_time = time.time()
    print(f"Redis (pipelined) - Temps de requêtage : {end_time - start_time:.6f} secondes")
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

# Fonction pour mesurer le temps de requêtage pour une relation one-to-many dans Redis (optimisée avec pipelining)
def query_redis_one_to_many():
    start_time = time.time()
    pipe = redis_client.pipeline()
    for produit in redis_client.keys("produit:*"):
        produit_data = redis_client.hgetall(produit)
        produit_id = produit.split(":")[1]
        variantes = redis_client.keys(f"variante:*:{produit_id}")
        for variante in variantes:
            pipe.hgetall(variante)
    rows = pipe.execute()
    end_time = time.time()
    print(f"Redis (one-to-many, pipelined) - Temps de requêtage : {end_time - start_time:.6f} secondes")
    return rows

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

    # Updated one-to-many query logic for Redis
    print("\nRequêtage one-to-many dans Redis :")
    start_redis_one_to_many = time.perf_counter()
    pipe = redis_client.pipeline()

    # Fetch all products
    produit_keys = redis_client.keys("produit:*")
    for produit_key in produit_keys:
        produit_data = redis_client.hgetall(produit_key)
        produit_id = produit_key.split(":")[1]

        # Fetch all variants for the current product
        variante_keys = redis_client.keys(f"variante:*")
        for variante_key in variante_keys:
            variante_data = redis_client.hgetall(variante_key)
            if variante_data.get("produit_id") == produit_id:
                pipe.hgetall(variante_key)

    redis_one_to_many_results = pipe.execute()
    end_redis_one_to_many = time.perf_counter()
    print(f"Redis (one-to-many, pipelined) - Temps de requêtage : {end_redis_one_to_many - start_redis_one_to_many:.6f} secondes")
    print(redis_one_to_many_results)

# Fermeture des connexions
pg_cursor.close()
pg_conn.close()