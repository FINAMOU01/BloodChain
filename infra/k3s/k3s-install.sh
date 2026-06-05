#!/bin/bash
set -euo pipefail

VPS_IP="207.180.220.145"
NAMESPACE="bloodchain"
MANIFESTS_DIR="/opt/bloodchain/infra/k3s/manifests"

SSH_CMD="ssh -o StrictHostKeyChecking=no root@${VPS_IP}"

echo "=========================================="
echo "  BloodChain K3s Deployment"
echo "  Target: ${VPS_IP}"
echo "  Namespace: ${NAMESPACE}"
echo "=========================================="

# --------------------------------------------------
# Step 0: Create remote manifests directory
# --------------------------------------------------
echo ""
echo "[0/9] Creating remote manifests directory..."
${SSH_CMD} "mkdir -p ${MANIFESTS_DIR}"
echo "✅ Done"

# --------------------------------------------------
# Step 1: Copy manifests to VPS
# --------------------------------------------------
echo "[1/9] Copying Kubernetes manifests to VPS..."
scp -o StrictHostKeyChecking=no \
  infra/k3s/manifests/*.yaml \
  root@${VPS_IP}:${MANIFESTS_DIR}/
echo "✅ Done"

# --------------------------------------------------
# Step 2: Create namespace
# --------------------------------------------------
echo "[2/9] Creating namespace '${NAMESPACE}'..."
${SSH_CMD} "kubectl apply -f ${MANIFESTS_DIR}/namespace.yaml"
echo "✅ Done"

# --------------------------------------------------
# Step 3: Create secrets
# --------------------------------------------------
echo "[3/9] Creating Kubernetes secrets..."
${SSH_CMD} "kubectl apply -f ${MANIFESTS_DIR}/secrets.yaml"
echo "✅ Done"

# --------------------------------------------------
# Step 4: Deploy databases (postgres, mongodb, redis, clickhouse)
# --------------------------------------------------
echo "[4/9] Deploying databases..."

deploy_and_wait() {
    local name=$1
    local file=$2
    echo "  → Deploying ${name}..."
    ${SSH_CMD} "kubectl apply -f ${MANIFESTS_DIR}/${file}" || {
        echo "  ❌ Failed to apply ${file}"
        return 1
    }
    echo "  ⏳ Waiting for ${name} to be ready..."
    ${SSH_CMD} "kubectl wait --for=condition=ready pod \
        -l app=${name} -n ${NAMESPACE} --timeout=120s" && \
    echo "  ✅ ${name} is ready" || \
    echo "  ⚠️  ${name} pod not ready within timeout, continuing..."
}

deploy_and_wait "postgres" "postgres-deployment.yaml"
deploy_and_wait "mongodb" "mongodb-deployment.yaml"
deploy_and_wait "redis" "redis-deployment.yaml"
deploy_and_wait "clickhouse" "clickhouse-deployment.yaml"

echo "✅ Databases deployed"

# --------------------------------------------------
# Step 5: Deploy application services
# --------------------------------------------------
echo "[5/9] Deploying application services..."

SERVICES=(
    "frontend-deployment.yaml"
    "user-management-deployment.yaml"
    "donor-deployment.yaml"
    "hospital-deployment.yaml"
    "blood-tracking-deployment.yaml"
    "notifications-deployment.yaml"
    "rewards-deployment.yaml"
    "location-deployment.yaml"
    "blockchain-gateway-deployment.yaml"
    "data-warehouse-deployment.yaml"
)

for svc_file in "${SERVICES[@]}"; do
    svc_name=$(echo "${svc_file}" | sed 's/-deployment.yaml//')
    echo "  → Deploying ${svc_name}..."
    ${SSH_CMD} "kubectl apply -f ${MANIFESTS_DIR}/${svc_file}" || {
        echo "  ❌ Failed to apply ${svc_file}"
        continue
    }
done

echo "✅ Services deployed"

# --------------------------------------------------
# Step 6: Wait for all service rollouts
# --------------------------------------------------
echo "[6/9] Waiting for all service rollouts to complete..."
for svc_file in "${SERVICES[@]}"; do
    svc_name=$(echo "${svc_file}" | sed 's/-deployment.yaml//')
    echo "  → Checking ${svc_name}..."
    ${SSH_CMD} "kubectl rollout status deployment/${svc_name} \
        -n ${NAMESPACE} --timeout=120s" && \
    echo "  ✅ ${svc_name} rolled out" || \
    echo "  ⚠️  ${svc_name} rollout not complete within timeout"
done

echo "✅ All rollouts checked"

# --------------------------------------------------
# Step 7: Deploy ingress
# --------------------------------------------------
echo "[7/9] Deploying Traefik Ingress..."
${SSH_CMD} "kubectl apply -f ${MANIFESTS_DIR}/ingress.yaml"
echo "✅ Done"

# --------------------------------------------------
# Step 8: Deploy network policies
# --------------------------------------------------
echo "[8/9] Deploying NetworkPolicies..."
${SSH_CMD} "kubectl apply -f ${MANIFESTS_DIR}/network-policies.yaml"
echo "✅ Done"

# --------------------------------------------------
# Step 9: Verify deployment
# --------------------------------------------------
echo "[9/9] Verifying deployment..."
echo ""
echo "--- Pods ---"
${SSH_CMD} "kubectl get pods -n ${NAMESPACE}" || echo "  (unable to list pods)"
echo ""
echo "--- Services ---"
${SSH_CMD} "kubectl get svc -n ${NAMESPACE}" || echo "  (unable to list services)"
echo ""
echo "--- Ingress ---"
${SSH_CMD} "kubectl get ingress -n ${NAMESPACE}" || echo "  (unable to list ingresses)"

echo ""
echo "=========================================="
echo "  BloodChain K3s deployment complete!"
echo "=========================================="
echo ""
echo "Check pod status with:"
echo "  ssh root@${VPS_IP} 'kubectl get pods -n ${NAMESPACE}'"
echo ""
echo "View logs with:"
echo "  ssh root@${VPS_IP} 'kubectl logs -n ${NAMESPACE} <pod-name>'"
echo ""
