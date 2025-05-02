# Mise en place de PostgreSQL avec réplication

Ce document explique les étapes nécessaires pour configurer un système de réplication PostgreSQL avec une instance principale et une instance secondaire à l'aide de Docker Compose.

## Étape 1 : Installer PostgreSQL sur deux conteneurs

1. **Création du fichier `docker-compose.yml`** :
   - Nous avons créé un fichier `docker-compose.yml` pour définir deux services :
     - `primary` : Instance principale de PostgreSQL.
     - `replica` : Instance secondaire de PostgreSQL.
   - Commande utilisée pour démarrer les conteneurs :
     ```bash
     docker-compose up -d
     ```

2. **Structure du fichier `docker-compose.yml`** :
   - Chaque service utilise un volume distinct pour stocker ses données :
     - `./primary` pour l'instance principale.
     - `./replica` pour l'instance secondaire.

## Étape 2 : Configurer l’instance principale pour activer la réplication

1. **Modifier `postgresql.conf`** :
   - **Pourquoi** : Ces paramètres activent la réplication en configurant le niveau de journalisation (`wal_level`), le nombre maximum d'expéditeurs de journaux (`max_wal_senders`), et la taille des journaux conservés (`wal_keep_size`).
   - **Comment** : Ajoutez les lignes suivantes dans `primary/postgresql.conf` :
     ```conf
     wal_level = replica
     max_wal_senders = 5
     wal_keep_size = 64
     ```

2. **Modifier `pg_hba.conf`** :
   - **Pourquoi** : Cette modification autorise les connexions de réplication depuis l'instance secondaire en utilisant l'utilisateur `postgres`.
   - **Comment** : Ajoutez la ligne suivante dans `primary/pg_hba.conf` :
     ```conf
     host replication postgres 0.0.0.0/0 md5
     ```

3. **Redémarrer l'instance principale** :
   - **Pourquoi** : Le redémarrage applique les modifications effectuées dans les fichiers de configuration.
   - **Comment** : Utilisez la commande suivante :
     ```bash
     docker-compose restart primary
     ```

## Étape 3 : Configurer l’instance secondaire pour recevoir les mises à jour

1. **Vider le répertoire de données** :
   - **Pourquoi** : Cela garantit que l'instance secondaire démarre avec une copie propre des données de l'instance principale.
   - **Comment** : Exécutez la commande suivante :
     ```bash
     docker exec -it tpredisdrkarra-replica-1 bash -c "rm -rf /var/lib/postgresql/data/*"
     ```

2. **Synchroniser les données avec `pg_basebackup`** :
   - **Pourquoi** : Cette commande copie les données de l'instance principale vers l'instance secondaire et configure automatiquement la réplication.
   - **Comment** : Exécutez la commande suivante :
     ```bash
     docker exec -it tpredisdrkarra-replica-1 bash -c "pg_basebackup -h tpredisdrkarra-primary-1 -D /var/lib/postgresql/data -U postgres -Fp -Xs -P -R"
     ```

3. **Configurer l'authentification sans mot de passe** :
   - **Pourquoi** : Le fichier `.pgpass` permet à l'instance secondaire de se connecter automatiquement à l'instance principale sans demander de mot de passe.
   - **Comment** : Créez et configurez le fichier `.pgpass` avec les commandes suivantes :
     ```bash
     docker exec -it tpredisdrkarra-replica-1 bash -c "echo 'tpredisdrkarra-primary-1:5432:*:postgres:postgres' > /var/lib/postgresql/.pgpass"
     docker exec -it tpredisdrkarra-replica-1 bash -c "chmod 600 /var/lib/postgresql/.pgpass"
     ```

4. **Redémarrer l'instance secondaire** :
   - **Pourquoi** : Le redémarrage applique les modifications et démarre l'instance secondaire en mode réplication.
   - **Comment** : Utilisez la commande suivante :
     ```bash
     docker-compose restart replica
     ```

## Étape 4 : Vérifier la synchronisation des données

1. **Insertion de données dans l'instance principale** :
   - Commande pour accéder à l'instance principale :
     ```bash
     docker exec -it tpredisdrkarra-primary-1 psql -U postgres
     ```
   - SQL exécuté :
     ```sql
     CREATE TABLE test_replication (id SERIAL PRIMARY KEY, data TEXT);
     INSERT INTO test_replication (data) VALUES ('Hello from primary');
     ```

2. **Vérification des données dans l'instance secondaire** :
   - Commande pour accéder à l'instance secondaire :
     ```bash
     docker exec -it tpredisdrkarra-replica-1 psql -U postgres
     ```
   - SQL exécuté :
     ```sql
     SELECT * FROM test_replication;
     ```

Si les données sont présentes dans l'instance secondaire, la réplication est configurée avec succès.

## Partie 2 : Utilisation de Redis pour optimiser les performances

Redis est utilisé comme un cache pour une table spécifique dans PostgreSQL. Cela permet de réduire la charge sur la base relationnelle en stockant les données en mémoire.

### Étape 1 : Installer Redis

1. **Ajout de Redis dans `docker-compose.yml`** :
   - Un service Redis a été ajouté au fichier `docker-compose.yml`.
   - Commande utilisée pour démarrer Redis :
     ```bash
     docker-compose up -d
     ```

2. **Structure mise à jour dans `docker-compose.yml`** :
   - Un service nommé `redis` a été ajouté avec le port `6379` exposé.

### Étape 2 : Configurer une connexion entre PostgreSQL et Redis

1. **Création du script `connect_postgres_redis.py`** :
   - Ce script connecte PostgreSQL et Redis.
   - Il lit les données de PostgreSQL et les stocke dans Redis.

2. **Installation des dépendances Python** :
   - Commande utilisée pour installer les bibliothèques nécessaires :
     ```bash
     pip install psycopg2 redis
     ```

### Étape 3 : Créer une table `taux_de_change` dans PostgreSQL et y insérer des données

1. **Création de la table** :
   - Commande SQL utilisée :
     ```sql
     CREATE TABLE taux_de_change (
         id SERIAL PRIMARY KEY,
         devise TEXT NOT NULL,
         taux NUMERIC NOT NULL
     );
     ```

2. **Insertion des données** :
   - Commande SQL utilisée :
     ```sql
     INSERT INTO taux_de_change (devise, taux) VALUES
     ('USD', 1.2),
     ('EUR', 1.1),
     ('GBP', 0.9),
     ('JPY', 135.0);
     ```

### Étape 4 : Comparer les temps de requêtage entre PostgreSQL et Redis

1. **Création du script `compare_query_times.py`** :
   - Ce script mesure les temps de requêtage pour PostgreSQL et Redis.

2. **Exécution du script** :
   - Commande utilisée :
     ```bash
     python compare_query_times.py
     ```

### Étape 5 : Essayer la même démarche avec deux tables (one-to-many)

1. **Création des tables `produits` et `variantes`** :
   - Commandes SQL utilisées :
     ```sql
     CREATE TABLE produits (
         id SERIAL PRIMARY KEY,
         nom TEXT NOT NULL
     );

     CREATE TABLE variantes (
         id SERIAL PRIMARY KEY,
         produit_id INT REFERENCES produits(id) ON DELETE CASCADE,
         nom TEXT NOT NULL,
         prix NUMERIC NOT NULL
     );
     ```

2. **Insertion des données** :
   - Commandes SQL utilisées :
     ```sql
     INSERT INTO produits (nom) VALUES
     ('Produit A'),
     ('Produit B'),
     ('Produit C');

     INSERT INTO variantes (produit_id, nom, prix) VALUES
     (1, 'Variante A1', 10.0),
     (1, 'Variante A2', 12.0),
     (2, 'Variante B1', 15.0),
     (3, 'Variante C1', 20.0),
     (3, 'Variante C2', 25.0);
     ```

3. **Synchronisation des données dans Redis** :
   - La fonction `sync_one_to_many` du script `connect_postgres_redis.py` a été utilisée pour synchroniser les données.

4. **Comparaison des temps de requêtage** :
   - Le script `compare_query_times.py` a été utilisé pour mesurer les performances des requêtes one-to-many.

   - Commande utilisée :
     ```bash
     python compare_query_times.py
     ```

## Partie 3 : Synchronisation des données entre PostgreSQL et Redis

Dans cette partie, nous avons mis en place un mécanisme pour synchroniser les données entre PostgreSQL et Redis en temps réel.

### Étape 1 : Supprimer la dépendance à `dblink` dans `sync_to_redis`

1. **Suppression du déclencheur `sync_taux_de_change`** :
   - Commande SQL utilisée :
     ```sql
     DROP TRIGGER IF EXISTS sync_taux_de_change ON taux_de_change;
     ```

2. **Suppression de la fonction `sync_to_redis`** :
   - Commande SQL utilisée :
     ```sql
     DROP FUNCTION IF EXISTS sync_to_redis();
     ```

### Étape 2 : Utilisation de `NOTIFY` et `LISTEN` pour envoyer et écouter des notifications

1. **Création de la fonction `notify_change`** :
   - Cette fonction envoie des notifications sur le canal `taux_de_change_channel` lors des modifications dans la table `taux_de_change`.
   - Commande SQL utilisée :
     ```sql
     CREATE OR REPLACE FUNCTION notify_change()
     RETURNS TRIGGER AS $$
     DECLARE
         payload TEXT;
     BEGIN
         IF (TG_OP = 'INSERT') THEN
             payload := FORMAT('INSERT:%s:%s:%s', NEW.id, NEW.devise, NEW.taux);
         ELSIF (TG_OP = 'UPDATE') THEN
             payload := FORMAT('UPDATE:%s:%s:%s', NEW.id, NEW.devise, NEW.taux);
         ELSIF (TG_OP = 'DELETE') THEN
             payload := FORMAT('DELETE:%s', OLD.id);
         END IF;

         PERFORM pg_notify('taux_de_change_channel', payload);
         RETURN NULL;
     END;
     $$ LANGUAGE plpgsql;
     ```

2. **Création du déclencheur `notify_taux_de_change`** :
   - Commande SQL utilisée :
     ```sql
     CREATE TRIGGER notify_taux_de_change
     AFTER INSERT OR UPDATE OR DELETE ON taux_de_change
     FOR EACH ROW
     EXECUTE FUNCTION notify_change();
     ```

### Étape 3 : Création du script Python `listen_and_sync.py`

1. **Fonctionnalités du script** :
   - Écoute des notifications PostgreSQL sur le canal `taux_de_change_channel`.
   - Synchronisation des données dans Redis en fonction des notifications reçues.

2. **Exécution du script** :
   - Commande utilisée :
     ```bash
     python listen_and_sync.py
     ```

3. **Exemple de test** :
   - Insérer une nouvelle ligne dans PostgreSQL :
     ```sql
     INSERT INTO taux_de_change (devise, taux) VALUES ('CAD', 0.8);
     ```
   - Mettre à jour une ligne existante :
     ```sql
     UPDATE taux_de_change SET taux = 1.5 WHERE devise = 'EUR';
     ```
   - Supprimer une ligne :
     ```sql
     DELETE FROM taux_de_change WHERE devise = 'USD';
     ```

4. **Vérification dans Redis** :
   - Utilisez `redis-cli` pour vérifier les données synchronisées :
     ```bash
     docker exec -it redis-server redis-cli
     KEYS taux_de_change:*
     HGETALL taux_de_change:<id>
     ```

### Note : Remplacement de `sync_triggers.sql` par `listen_and_sync.py`

Le fichier `sync_triggers.sql`, qui utilisait la fonction `sync_to_redis` pour synchroniser directement PostgreSQL et Redis, n'est plus nécessaire. 

À la place, nous utilisons le script Python `listen_and_sync.py`, qui écoute les notifications PostgreSQL via `NOTIFY` et met à jour Redis en conséquence. 

Cela offre une solution plus flexible et découplée, permettant une meilleure gestion des mises à jour entre PostgreSQL et Redis.

### Suppression des fichiers inutiles

Le fichier `sync_triggers.sql` a été supprimé car il n'est plus nécessaire pour ce projet. La synchronisation entre PostgreSQL et Redis est désormais gérée par le script Python `listen_and_sync.py`.

## Partie 4 : Expérimentations et Analyse des performances

1. **Développement d'un Web Service REST** :
   - Création du fichier `web_service.py` avec Flask.
   - Endpoints :
     - `/query_postgres` : Interroge PostgreSQL.
     - `/query_redis` : Interroge Redis.
   - Commande pour exécuter le service :
     ```bash
     python web_service.py
     ```

2. **Benchmark des performances** :
   - Création du script `benchmark_requests.py` pour mesurer les temps de réponse.
   - Commande pour exécuter le benchmark :
     ```bash
     python benchmark_requests.py
     ```

3. **Simulation de panne de l’instance primaire** :
   - Arrêt de l'instance primaire avec :
     ```bash
     docker-compose stop primary
     ```
   - Observation du comportement de l'instance secondaire :
     - Vérification que les requêtes en lecture fonctionnent.
     - Confirmation que les écritures échouent (mode read-only).
   - Redémarrage de l'instance primaire avec :
     ```bash
     docker-compose start primary
     ```
   - Vérification de la reprise de la réplication :
     - Insertion de nouvelles données dans l'instance primaire.
     - Vérification de la synchronisation dans l'instance secondaire.

## Partie 5 : Critique de l'architecture et proposition d'une solution alternative moderne

### Critique de l'architecture actuelle

1. **Points positifs** :
   - **Répartition des charges** : L'utilisation de Redis comme cache réduit la charge sur PostgreSQL pour les requêtes fréquentes.
   - **Réplication PostgreSQL** : La réplication assure une haute disponibilité et une tolérance aux pannes.
   - **Flexibilité** : L'intégration de `NOTIFY` et `LISTEN` avec un script Python permet une synchronisation en temps réel entre PostgreSQL et Redis.
   - **Web Service REST** : Fournit une interface simple pour interroger PostgreSQL et Redis.

2. **Limites** :
   - **Couplage fort** : La synchronisation entre PostgreSQL et Redis repose sur un script Python (`listen_and_sync.py`), ce qui peut être difficile à maintenir à grande échelle.
   - **Manque de scalabilité** : L'architecture actuelle ne gère pas bien les charges massives ou les scénarios multi-régions.
   - **Redis comme cache manuel** : La gestion manuelle des données dans Redis peut entraîner des incohérences si des erreurs surviennent.
   - **Absence d'orchestration avancée** : L'utilisation de Docker Compose est limitée pour des environnements complexes ou multi-nœuds.

### Proposition d'une solution alternative moderne

1. **Utilisation d'un système de cache distribué avancé** :
   - Remplacez Redis par **Amazon ElastiCache** (Redis géré) ou **Memcached** pour une gestion simplifiée et une scalabilité automatique.
   - **Avantage** : Réduction de la charge opérationnelle et meilleure gestion des données en mémoire.

2. **Adoption d'un orchestrateur de conteneurs** :
   - Remplacez Docker Compose par **Kubernetes** pour une meilleure gestion des conteneurs, des déploiements, et de la scalabilité.
   - **Avantage** : Gestion avancée des ressources, tolérance aux pannes, et déploiements multi-régions.

3. **Utilisation d'un outil de synchronisation natif** :
   - Intégrez **Debezium** pour capturer les changements dans PostgreSQL et les propager automatiquement à Redis via Kafka.
   - **Avantage** : Découplage complet entre PostgreSQL et Redis, avec une gestion des événements en temps réel.

4. **Migration vers une base de données hybride** :
   - Utilisez une base de données comme **Amazon Aurora** ou **CockroachDB** qui combine les avantages des bases relationnelles et des caches en mémoire.
   - **Avantage** : Réduction de la complexité en éliminant le besoin d'un cache séparé.

5. **Amélioration du Web Service** :
   - Remplacez Flask par un framework plus robuste comme **FastAPI** pour des performances accrues et une meilleure gestion des API.
   - Intégrez un outil de monitoring comme **Prometheus** pour surveiller les performances des endpoints.

### Conclusion
L'architecture actuelle est fonctionnelle pour des charges légères à modérées, mais elle présente des limites en termes de scalabilité et de maintenance. Une solution moderne basée sur des outils comme Kubernetes, Debezium, et des services managés (ElastiCache, Aurora) offrirait une meilleure résilience, scalabilité, et simplicité opérationnelle.