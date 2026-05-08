# BloodChain Nginx Reverse Proxy

## Purpose
This Nginx configuration routes requests to the different backend microservices.

## Services

| Service | Route | Port |
|----------|-------|------|
| Frontend | / | 8000 |
| User Management | /api/users/ | 8001 |
| Donor Service | /api/donors/ | 8002 |
| Hospital Service | /api/hospitals/ | 8003 |
| Blood Tracking | /api/tracking/ | 8004 |
| Notifications | /api/notifications/ | 8005 |
| Rewards | /api/rewards/ | 8006 |
| Location | /api/location/ | 8007 |
| Blockchain Gateway | /api/blockchain/ | 8008 |
| Analytics | /api/analytics/ | 8009 |

## Reload Nginx

```bash
sudo systemctl reload nginx