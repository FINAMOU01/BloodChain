# Prometheus + Grafana Installation for BloodChain

This guide covers deploying Prometheus and Grafana on the K3s cluster alongside the BloodChain microservices.

## Prerequisites

- K3s cluster running on `207.180.220.145`
- `kubectl` configured to access the cluster
- Namespace `bloodchain` already created
- All BloodChain services deployed and exposing `/metrics/`

## Step 1: Create Monitoring Namespace

```bash
ssh root@207.180.220.145 'kubectl create namespace monitoring'
```

## Step 2: Deploy Prometheus

Create a file `prometheus-deployment.yaml`:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: prometheus-pvc
  namespace: monitoring
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: local-path
  resources:
    requests:
      storage: 10Gi
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s

    scrape_configs:
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
            action: replace
            target_label: __metrics_path__
            regex: (.+)
          - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
            action: replace
            regex: ([^:]+)(?::\d+)?;(\d+)
            replacement: $1:$2
            target_label: __address__
          - source_labels: [__meta_kubernetes_pod_label_app]
            target_label: service
          - source_labels: [__meta_kubernetes_namespace]
            target_label: namespace

      - job_name: 'postgres'
        static_configs:
          - targets: ['postgres.bloodchain.svc.cluster.local:9187']

      - job_name: 'redis'
        static_configs:
          - targets: ['redis.bloodchain.svc.cluster.local:9121']

      - job_name: 'mongodb'
        static_configs:
          - targets: ['mongodb.bloodchain.svc.cluster.local:9216']

    rule_files:
      - /etc/prometheus/alert_rules.yml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
        - name: prometheus
          image: prom/prometheus:v2.53.0
          args:
            - '--config.file=/etc/prometheus/prometheus.yml'
            - '--storage.tsdb.path=/prometheus'
            - '--storage.tsdb.retention.time=30d'
          ports:
            - containerPort: 9090
          volumeMounts:
            - name: config
              mountPath: /etc/prometheus
            - name: data
              mountPath: /prometheus
            - name: alert-rules
              mountPath: /etc/prometheus/alert_rules.yml
              subPath: alert_rules.yml
      volumes:
        - name: config
          configMap:
            name: prometheus-config
        - name: data
          persistentVolumeClaim:
            claimName: prometheus-pvc
        - name: alert-rules
          configMap:
            name: prometheus-alert-rules
---
apiVersion: v1
kind: Service
metadata:
  name: prometheus
  namespace: monitoring
spec:
  ports:
    - port: 9090
      targetPort: 9090
  selector:
    app: prometheus
```

Apply it:

```bash
# Copy alert_rules.yml to the VPS first
scp infra/monitoring/alert_rules.yml root@207.180.220.145:/tmp/

# Create alert rules ConfigMap
ssh root@207.180.220.145 \
  'kubectl create configmap prometheus-alert-rules \
     --namespace monitoring \
     --from-file=/tmp/alert_rules.yml'

# Deploy Prometheus
ssh root@207.180.220.145 'kubectl apply -f -' < infra/k3s/prometheus-deployment.yaml
```

## Step 3: Deploy Grafana

Create a file `grafana-deployment.yaml`:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: grafana-pvc
  namespace: monitoring
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: local-path
  resources:
    requests:
      storage: 5Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      containers:
        - name: grafana
          image: grafana/grafana:11.1.0
          ports:
            - containerPort: 3000
          env:
            - name: GF_SERVER_ROOT_URL
              value: http://207.180.220.145/grafana/
            - name: GF_SERVER_SERVE_FROM_SUB_PATH
              value: "true"
            - name: GF_AUTH_ANONYMOUS_ENABLED
              value: "true"
            - name: GF_SECURITY_ADMIN_USER
              value: admin
            - name: GF_SECURITY_ADMIN_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: grafana-admin
                  key: password
          volumeMounts:
            - name: data
              mountPath: /var/lib/grafana
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: grafana-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: grafana
  namespace: monitoring
spec:
  ports:
    - port: 3000
      targetPort: 3000
  selector:
    app: grafana
```

Create the admin secret and deploy:

```bash
ssh root@207.180.220.145 \
  'kubectl create secret generic grafana-admin \
     --namespace monitoring \
     --from-literal=password=bloodchain-monitor-2026'

ssh root@207.180.220.145 'kubectl apply -f -' < path/to/grafana-deployment.yaml
```

## Step 4: Apply Ingress

```bash
kubectl apply -f infra/monitoring/grafana-ingress.yaml
```

## Step 5: Verify

```bash
ssh root@207.180.220.145 'kubectl get pods -n monitoring'
```

Expected output:
```
NAME                          READY   STATUS    RESTARTS   AGE
prometheus-xxxxx              1/1     Running   0          1m
grafana-xxxxx                 1/1     Running   0          1m
```

## Accessing the Dashboards

| Service   | URL                                | Default Credentials     |
|-----------|------------------------------------|-------------------------|
| Prometheus| `http://207.180.220.145:9090`      | None (no auth)          |
| Grafana   | `http://207.180.220.145/grafana/`  | admin / bloodchain-monitor-2026 |

## Adding Prometheus Data Source in Grafana

1. Log in to Grafana (`admin / bloodchain-monitor-2026`)
2. Go to **Configuration → Data Sources → Add data source**
3. Select **Prometheus**
4. Set URL to `http://prometheus.monitoring.svc.cluster.local:9090`
5. Click **Save & Test**

## Recommended Dashboards

| Dashboard                        | Grafana ID |
|----------------------------------|------------|
| Django Prometheus Statistics     | 17650      |
| Node Exporter Full               | 1860       |
| Redis Dashboard                  | 12776      |
| PostgreSQL                      | 9628       |
| Kubernetes Pod Metrics           | 15761      |

To import:
1. Grafana → **+ → Import**
2. Enter the dashboard ID
3. Select Prometheus data source
4. Click **Import**

## Troubleshooting

**Prometheus cannot scrape services:**
Ensure each Django service has `django_prometheus` in `INSTALLED_APPS` and annotation `prometheus.io/scrape: "true"` on the pod template.

**Grafana returns 404 on /grafana/:**
Make sure `GF_SERVER_ROOT_URL` and `GF_SERVER_SERVE_FROM_SUB_PATH` are configured correctly in the Grafana deployment.

**No data in Grafana:**
Check Prometheus targets at `http://207.180.220.145:9090/targets` to confirm services are being scraped.
