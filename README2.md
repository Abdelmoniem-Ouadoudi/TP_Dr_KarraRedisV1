# Questions and Answers for the Project

This document contains potential questions about the project and their corresponding answers to help prepare for discussions or evaluations.

---

### **General Questions**

1. **What is the purpose of this project?**
   - The project aims to integrate PostgreSQL and Redis to optimize database performance, ensure data synchronization, and analyze system behavior under different scenarios. It includes replication, caching, and performance benchmarking.

2. **Why did you choose Redis as a cache?**
   - Redis is an in-memory data store that provides extremely fast read and write operations. It reduces the load on PostgreSQL by caching frequently accessed data, improving response times for repetitive queries.

3. **What are the main components of your architecture?**
   - **PostgreSQL**: Primary and replica instances for data storage and replication.
   - **Redis**: Used as a cache to optimize query performance.
   - **Web Service REST**: Provides endpoints to query PostgreSQL and Redis.
   - **Python Scripts**: Handle synchronization (`listen_and_sync.py`), benchmarking (`benchmark_requests.py`), and data comparison (`compare_data_sync.py`).

---

### **Technical Questions**

4. **How does the replication between the primary and secondary PostgreSQL instances work?**
   - Replication is achieved using `pg_basebackup` for initial synchronization and WAL (Write-Ahead Logging) for continuous updates. The secondary instance operates in read-only mode and receives updates from the primary instance.

5. **How does the `listen_and_sync.py` script work?**
   - The script listens to PostgreSQL notifications via the `LISTEN` command. When a notification is received, it processes the payload and updates Redis accordingly (e.g., adding, updating, or deleting keys).

6. **What is the role of the `notify_change` function in PostgreSQL?**
   - This function sends notifications using the `NOTIFY` command whenever data in the `taux_de_change` table is modified. It includes details about the operation (INSERT, UPDATE, DELETE) and the affected data.

7. **How do you ensure data consistency between PostgreSQL and Redis?**
   - Data consistency is ensured by treating PostgreSQL as the source of truth. The `listen_and_sync.py` script updates Redis in real-time based on PostgreSQL notifications. The `compare_data_sync.py` script is used to periodically verify synchronization.

8. **What is the purpose of the Web Service REST?**
   - The Web Service REST provides endpoints (`/query_postgres` and `/query_redis`) to query PostgreSQL and Redis. It is used for performance benchmarking and external access to the data.

---

### **Performance and Analysis Questions**

9. **What were the results of your performance benchmarking?**
   - Redis generally provides faster response times for repetitive queries due to its in-memory storage. However, PostgreSQL can be faster for complex queries or when the dataset is small.

10. **What happens when the primary PostgreSQL instance fails?**
    - The secondary instance remains operational in read-only mode, allowing queries to continue. Once the primary instance is restored, replication resumes, and the secondary instance is updated with any changes.

11. **Why is Redis slower in some cases compared to PostgreSQL?**
    - Redis may be slower if there is overhead in key lookups or data serialization/deserialization. Additionally, for small datasets, PostgreSQL's optimized query engine can outperform Redis.

---

### **Critique and Alternatives**

12. **What are the limitations of your current architecture?**
    - Manual cache management in Redis can lead to inconsistencies.
    - The reliance on Python scripts for synchronization adds complexity.
    - Docker Compose is limited in scalability and orchestration for large-scale deployments.

13. **What modern alternatives would you propose?**
    - Use **Kubernetes** for container orchestration.
    - Replace manual Redis management with **Amazon ElastiCache** or **Memcached**.
    - Use **Debezium** with Kafka for event-driven synchronization.
    - Consider hybrid databases like **Amazon Aurora** for built-in caching and replication.

14. **Why did you choose Flask for the Web Service?**
    - Flask is lightweight and easy to set up, making it suitable for small projects. For larger projects, frameworks like **FastAPI** could be used for better performance and scalability.

---

### **Practical and Debugging Questions**

15. **How would you debug synchronization issues between PostgreSQL and Redis?**
    - Use `redis-cli` to inspect Redis keys and values.
    - Check PostgreSQL logs for errors in the `notify_change` function.
    - Use the `compare_data_sync.py` script to identify discrepancies.

16. **How do you handle data conflicts between PostgreSQL and Redis?**
    - PostgreSQL is treated as the source of truth. Redis is only a cache, so any discrepancies are resolved by re-synchronizing from PostgreSQL.

17. **What happens if the `listen_and_sync.py` script crashes?**
    - Redis may temporarily become outdated. Restarting the script will resume synchronization. Periodic checks with `compare_data_sync.py` can ensure consistency.

---

### **Future Improvements**

18. **How would you scale this architecture for a production environment?**
    - Use **Kubernetes** for container orchestration.
    - Implement distributed caching with **Amazon ElastiCache**.
    - Use managed database services like **Amazon RDS** for PostgreSQL.

19. **What additional features could you add to the Web Service?**
    - Add authentication and authorization.
    - Implement logging and monitoring with tools like **Prometheus** and **Grafana**.
    - Add support for more complex queries and analytics.

20. **How would you monitor the health of your system?**
    - Use **Prometheus** for monitoring metrics (e.g., query response times, replication lag).
    - Use **Grafana** for visualizing system performance.
    - Set up alerts for failures or performance degradation.

---