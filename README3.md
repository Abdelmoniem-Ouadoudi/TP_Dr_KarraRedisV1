# Project Summary: PostgreSQL and Redis Integration

This document provides a summary of each part of the project and its purpose.

---

## **Partie 1: Mise en place de PostgreSQL avec réplication**

### **Summary**
In this part, we set up a PostgreSQL database with a primary instance and a replica instance. The replica is configured to receive updates from the primary instance using WAL (Write-Ahead Logging) for replication.

### **Purpose**
To ensure high availability and fault tolerance by maintaining a secondary read-only instance that can take over in case of primary instance failure.

---

## **Partie 2: Utilisation de Redis pour optimiser les performances**

### **Summary**
Redis is integrated as a caching layer to store frequently accessed data from PostgreSQL. Python scripts are used to synchronize data between PostgreSQL and Redis.

### **Purpose**
To reduce the load on PostgreSQL and improve query performance by serving repetitive queries from Redis.

---

## **Partie 3: Synchronisation des données entre PostgreSQL et Redis**

### **Summary**
A real-time synchronization mechanism is implemented using PostgreSQL's `NOTIFY` and `LISTEN` commands. A Python script listens for changes in PostgreSQL and updates Redis accordingly.

### **Purpose**
To ensure that Redis remains up-to-date with PostgreSQL, maintaining data consistency between the two systems.

---

## **Partie 4: Expérimentations et Analyse des performances**

### **Summary**
A Web Service REST is developed to query both PostgreSQL and Redis. Performance benchmarking is conducted to compare response times. Additionally, a primary instance failure is simulated to observe the behavior of the replica.

### **Purpose**
To analyze the performance of PostgreSQL and Redis under different scenarios and ensure the system's resilience during failures.

---

## **Partie 5: Critique de l'architecture et proposition d'une solution alternative moderne**

### **Summary**
The current architecture is reviewed, highlighting its strengths and limitations. Modern alternatives such as Kubernetes, Debezium, and managed services like Amazon ElastiCache are proposed to improve scalability and maintainability.

### **Purpose**
To identify areas for improvement in the architecture and suggest modern solutions for better scalability, resilience, and operational simplicity.

---