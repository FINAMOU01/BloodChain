# BloodChain Monitoring

This directory contains configuration files for monitoring the BloodChain microservices platform using **Prometheus** and **Grafana**.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Django Services │────▶│   Prometheus     │◀────│  Alertmanager │
│  (/metrics)      │     │  (scrape every    │     │              │
│                  │     │   15s)           │     │  (email,      │
│  Postgres        │     │                  │     │   webhook)    │
│  Redis           │     │  stores in:      │     └──────────────┘
│  MongoDB         │     │  /var/lib/       │
│  ClickHouse      │     │  prometheus/     │
└─────────────────┘     └────────┬─────────┘
                                 │
                                 ▼
                          ┌──────────────┐
                          │   Grafana    │
                          │  (port 3000) │
                          │              │
                          │ Dashboards:  │
                          │ - Service    │
                          │   Health     │
                          │ - API        │
                          │   Latency    │
                          │ - Database   │
                          │   Metrics    │
                          │ - Blockchain │
                          │   Events     │
                          └──────────────┘
```

## Components

| Component    | Description                                      | Port  |
|-------------|--------------------------------------------------|-------|
| Prometheus  | Metrics collection & alerting engine             | 9090  |
| Grafana     | Visualization dashboards                         | 3000  |
| Alertmanager| Alert routing & notification (optional)          | 9093  |

## How It Works

1. Every Django microservice includes `django_prometheus` in `INSTALLED_APPS` and exposes metrics at `/metrics/`.
2. Prometheus scrapes all service endpoints every 15 seconds.
3. Alert rules in `alert_rules.yml` trigger when conditions are met (e.g., service down, high latency).
4. Grafana queries Prometheus as its data source and renders dashboards.

## Files

| File                    | Description                                    |
|------------------------|------------------------------------------------|
| `README.md`            | This file — overview and setup instructions    |
| `prometheus-install.md`| Step-by-step Prometheus + Grafana installation |
| `grafana-ingress.yaml` | K3s Ingress to expose Grafana externally       |
| `alert_rules.yml`      | Prometheus alerting rules for BloodChain       |

## Quick Start

1. Install Prometheus and Grafana (see `prometheus-install.md`)
2. Apply the Grafana ingress:
   ```bash
   kubectl apply -f infra/monitoring/grafana-ingress.yaml
   ```
3. Access Grafana at `http://207.180.220.145/grafana/`
4. Add Prometheus data source: `http://prometheus:9090`
5. Import dashboards from the Grafana marketplace or create custom ones
