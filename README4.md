# Complete Project Documentation: PostgreSQL and Redis Integration

This document provides a detailed overview of the project, including its structure, purpose, and the roles of various files.

---

## **Partie 1: Mise en place de PostgreSQL avec réplication**

### **Summary**
In this part, we set up a PostgreSQL database with a primary instance and a replica instance. The replica is configured to receive updates from the primary instance using WAL (Write-Ahead Logging) for replication.

### **Purpose**
To ensure high availability and fault tolerance by maintaining a secondary read-only instance that can take over in case of primary instance failure.

### **Files Used**
- **`docker-compose.yml`**: Defines the services for the primary and replica PostgreSQL instances.
- **`primary/` and `replica/`**: Contain configuration files (`postgresql.conf`, `pg_hba.conf`) for the primary and replica instances.

---

## **Partie 2: Utilisation de Redis pour optimiser les performances**

### **Summary**
Redis is integrated as a caching layer to store frequently accessed data from PostgreSQL. Python scripts are used to synchronize data between PostgreSQL and Redis.

### **Purpose**
To reduce the load on PostgreSQL and improve query performance by serving repetitive queries from Redis.

### **Files Used**
- **`connect_postgres_redis.py`**: Connects PostgreSQL and Redis, synchronizing data from PostgreSQL to Redis.
- **`compare_query_times.py`**: Measures query times for PostgreSQL and Redis to analyze performance improvements.

### **Example Commands**
- Synchronize data:
  ```bash
  python connect_postgres_redis.py
  ```
- Compare query times:
  ```bash
  python compare_query_times.py
  ```

---

## **Partie 3: Synchronisation des données entre PostgreSQL et Redis**

### **Summary**
A real-time synchronization mechanism is implemented using PostgreSQL's `NOTIFY` and `LISTEN` commands. A Python script listens for changes in PostgreSQL and updates Redis accordingly.

### **Purpose**
To ensure that Redis remains up-to-date with PostgreSQL, maintaining data consistency between the two systems.

### **Files Used**
- **`listen_and_sync.py`**: Listens to PostgreSQL notifications and updates Redis in real-time.
- **`compare_data_sync.py`**: Compares data between PostgreSQL and Redis to verify synchronization.
- **`notify_listen.sql`**: Contains SQL commands to set up `NOTIFY` and `LISTEN` in PostgreSQL.

### **Example Commands**
- Start listening for changes:
  ```bash
  python listen_and_sync.py
  ```
- Compare data:
  ```bash
  python compare_data_sync.py
  ```

---

## **Partie 4: Expérimentations et Analyse des performances**

### **Summary**
A Web Service REST is developed to query both PostgreSQL and Redis. Performance benchmarking is conducted to compare response times. Additionally, a primary instance failure is simulated to observe the behavior of the replica.

### **Purpose**
To analyze the performance of PostgreSQL and Redis under different scenarios and ensure the system's resilience during failures.

### **Files Used**
- **`web_service.py`**: Implements a Web Service REST with endpoints to query PostgreSQL and Redis.
- **`benchmark_requests.py`**: Benchmarks the performance of PostgreSQL and Redis by sending repeated requests to the Web Service REST.

### **Example Commands**
- Start the Web Service:
  ```bash
  python web_service.py
  ```
- Benchmark performance:
  ```bash
  python benchmark_requests.py
  ```

---

## **Partie 5: Critique de l'architecture et proposition d'une solution alternative moderne**

### **Summary**
The current architecture is reviewed, highlighting its strengths and limitations. Modern alternatives such as Kubernetes, Debezium, and managed services like Amazon ElastiCache are proposed to improve scalability and maintainability.

### **Purpose**
To identify areas for improvement in the architecture and suggest modern solutions for better scalability, resilience, and operational simplicity.

---

## **Project Structure**

### **Main Files**
- **`docker-compose.yml`**: Defines the services for PostgreSQL and Redis.
- **`connect_postgres_redis.py`**: Synchronizes data from PostgreSQL to Redis.
- **`compare_query_times.py`**: Measures query times for PostgreSQL and Redis.
- **`compare_data_sync.py`**: Verifies data consistency between PostgreSQL and Redis.
- **`listen_and_sync.py`**: Listens for PostgreSQL changes and updates Redis.
- **`web_service.py`**: Provides REST endpoints to query PostgreSQL and Redis.
- **`benchmark_requests.py`**: Benchmarks the performance of PostgreSQL and Redis.
- **`notify_listen.sql`**: Sets up `NOTIFY` and `LISTEN` in PostgreSQL.

### **Configuration Folders**
- **`primary/`**: Configuration files for the primary PostgreSQL instance.
- **`replica/`**: Configuration files for the replica PostgreSQL instance.

---