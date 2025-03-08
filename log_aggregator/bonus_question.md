# High-Level Architecture

## 1. Load Balancer

**Role:** Distributes inbound requests/logs across multiple Ingestion Servers  
**Why:** Ensures no single ingestion server becomes a bottleneck, and provides horizontal scalability.

---

## 2. Ingestion Servers (Cluster)

-   **Receive Logs:** Can accept logs via HTTP, TCP, or other protocols.
-   **Normalization:** Convert disparate log formats into a standard JSON schema.
-   **Database Write:** Persist raw logs to a durable database (or a queue/storage first, then the database).

---

## 3. Database Layer

### Scaling Options:

-   **Relational Database:** Scale vertically or use read replicas.
-   **NoSQL or Sharded SQL:** Distribute data across multiple nodes to handle large volumes.

**Purpose:** Provides reliable, persistent storage for all incoming logs.

---

## 4. Aggregator Services (Cluster)

-   **Pulling Data:** Read from the database (or a message queue).
-   **Aggregation & Analysis:**
    -   Run the Python script or a streaming framework (e.g., Apache Beam / Dataflow) to calculate metrics (requests/hour, top endpoints).
    -   Detect anomalies (spikes, error surges).
-   **Load Balancer (Internal):** An internal load balancer can distribute work to multiple aggregator service instances.

---

## 5. Alerts & Dashboards

### Alerts:

-   The aggregator services push detected anomalies to an alerting system (e.g., email, Slack, PagerDuty).

### Dashboards:

-   BI/Analytics tool (e.g., Looker Studio, Grafana) queries aggregated metrics from the DB or a data warehouse (like BigQuery).

---

## Flow Example

1. **Load Balancer (front-end)** receives log traffic from various web servers or applications.
2. **Ingestion Servers** process the logs in parallel, normalizing data, and writing it to the Database.
3. **Aggregator Services** continuously pull or subscribe to new data, process it, and store aggregated metrics/results.
4. **Alerts** are triggered if anomalies exceed configured thresholds.
5. **Dashboards** visualize real-time and historical metrics.

---

## Pros

### High Scalability & Availability

-   Front-End Load Balancer distributes traffic evenly, preventing a single ingestion server from being overloaded.
-   Aggregator Load Balancer allows the analysis layer to expand horizontally as data volumes increase.

### Modular & Decoupled

-   Each layer (ingestion, storage, aggregation) can scale independently, reducing overall system coupling.

### Resilience to Spikes

-   Automatic or semi-automatic scaling of ingestion and aggregator clusters can handle traffic bursts gracefully.

### Flexible Data Pipeline

-   The system can incorporate a queue (e.g., Pub/Sub, RabbitMQ) between ingestion and aggregation if real-time processing and buffering are needed.

---

## Cons

### Load Balancer Complexity & Cost

-   Additional infrastructure components (load balancers) introduce cost and operational overhead.

### Configuration Overhead

-   Balancing server pools, configuring health checks, and ensuring smooth autoscaling requires careful DevOps and monitoring.

### Potential Latency

-   Multiple hops (load balancer → ingestion servers → database → aggregator) can add latency if real-time analysis is critical.

### Database Scaling Complexity

-   Even with load-balanced ingestion, high write loads might require advanced partitioning, sharding, or using a distributed NoSQL solution.
