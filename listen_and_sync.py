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
pg_conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
pg_cursor = pg_conn.cursor()

# Connexion à Redis
redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)

# Fonction pour traiter les notifications PostgreSQL
def handle_notification(notification):
    payload = notification.payload
    operation, *data = payload.split(":")

    if operation == "INSERT" or operation == "UPDATE":
        id, devise, taux = data
        redis_client.hset(f"taux_de_change:{id}", mapping={"devise": devise, "taux": taux})
        print(f"Synchronisé dans Redis : taux_de_change:{id} -> {{'devise': '{devise}', 'taux': '{taux}'}}")

    elif operation == "DELETE":
        id = data[0]
        redis_client.delete(f"taux_de_change:{id}")
        print(f"Supprimé de Redis : taux_de_change:{id}")

# Écoute des notifications PostgreSQL
def listen_to_postgres():
    pg_cursor.execute("LISTEN taux_de_change_channel;")
    print("En attente des notifications sur le canal 'taux_de_change_channel'...")

    while True:
        pg_conn.poll()
        while pg_conn.notifies:
            notification = pg_conn.notifies.pop(0)
            handle_notification(notification)

if __name__ == "__main__":
    try:
        listen_to_postgres()
    except KeyboardInterrupt:
        print("Arrêt de l'écoute.")
    finally:
        pg_cursor.close()
        pg_conn.close()