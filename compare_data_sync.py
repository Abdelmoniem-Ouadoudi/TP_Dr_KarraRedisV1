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

def fetch_postgres_data():
    pg_cursor.execute("SELECT id, devise, taux FROM taux_de_change;")
    return {str(row[0]): {"devise": row[1], "taux": str(row[2])} for row in pg_cursor.fetchall()}

def fetch_redis_data():
    keys = redis_client.keys("taux_de_change:*")
    return {key.split(":")[1]: redis_client.hgetall(key) for key in keys}

def compare_data():
    postgres_data = fetch_postgres_data()
    redis_data = fetch_redis_data()

    print("Comparaison des données entre PostgreSQL et Redis :")

    all_good = True

    # Vérifier les données présentes dans PostgreSQL mais absentes dans Redis
    for id, data in postgres_data.items():
        if id not in redis_data:
            print(f"Donnée manquante dans Redis : {id} -> {data}")
            all_good = False
        elif redis_data[id] != data:
            print(f"Donnée différente pour l'ID {id} : PostgreSQL={data}, Redis={redis_data[id]}")
            all_good = False

    # Vérifier les données présentes dans Redis mais absentes dans PostgreSQL
    for id, data in redis_data.items():
        if id not in postgres_data:
            print(f"Donnée manquante dans PostgreSQL : {id} -> {data}")
            all_good = False

    if all_good:
        print("Toutes les données sont synchronisées entre PostgreSQL et Redis.")

if __name__ == "__main__":
    compare_data()

# Fermeture des connexions
pg_cursor.close()
pg_conn.close()