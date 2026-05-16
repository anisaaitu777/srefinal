@echo off
echo [SRE] Pulling latest configurations...
git pull origin main

echo [SRE] Applying manifests to local Kubernetes cluster...
kubectl apply -f deployment.yaml

echo [SRE] Checking rollout status...
kubectl rollout status deployment/srefinal-app -n srefinal-prod

echo [SRE] Deployment successfully completed!
pause