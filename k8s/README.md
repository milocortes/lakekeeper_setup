# Deploy Keycloak K8S



To create a Keycloak deployment on Kubernetes and automatically import a `realm.json` file using `kubectl`im going to use **ConfigMap** (traditional Kubernetes manifests).

Method 1: Using a ConfigMap (Standard Deployment)

This is the most straightforward method. You store the `realm.json` file inside a Kubernetes ConfigMap, mount it into the Keycloak container, and pass the `--import-realm` startup flag.

Step 1: Create the ConfigMap

Run the following `kubectl` command to wrap your `realm.json` into a ConfigMap resource: 

 ```bash
 kubectl create configmap keycloak-realm-import --from-file=realm.json
 ```



Step 2: Configure your `deployment.yaml`

Mount the ConfigMap to `/opt/keycloak/data/import/` (the default directory Keycloak checks) and add the `--import-realm` argument.



```bash
minikube start
kubectl cluster-info
kubectl get nodes
kubectl create namespace lakekeeper
kubectl config set-context --current --namespace=lakekeeper
kubectl get ns
kubectl create configmap keycloak-realm-import --from-file=realm.json
kubectl create -f keycloak.yaml
kubectl get pods
kubectl  describe pod keycloak
kubectl logs -f
kubectl get svc keycloak
kubectl port-forward svc/keycloak -n default 30080:8080
kubectl port-forward svc/postgres -n default 5432:5432
```

