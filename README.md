# Cloud-Native DevOps — Order Processing Platform

A microservices-based Order Processing Platform demonstrating a complete Cloud-Native DevOps workflow using **FastAPI, Docker, Kubernetes, Helm, GitHub Actions, and Terraform**.

The project is designed for deployment to **Azure Kubernetes Service (AKS)** with **Azure Container Registry (ACR)**. Since an Azure subscription was not available during implementation, the application was fully containerized, tested, and deployed locally using **Minikube**.

---

## Architecture

```text
                         Developer
                             |
                             v
                    +----------------+
                    |    GitHub      |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    | GitHub Actions  |
                    |   CI / Tests    |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    | Docker Images   |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    | Helm Chart      |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    | Kubernetes      |
                    |   (Minikube)   |
                    +-------+--------+
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
        +-----------+ +-----------+ +----------------+
        | Order API | |   Order   | | Notification   |
        |           | | Processor | |    Service     |
        +-----------+ +-----------+ +----------------+
```

### Application Flow

```text
Client
  |
  v
Order API
  |
  v
Order Processor
  |
  v
Notification Service
```

---

## Services

| Service              | Description                             | Port |
| -------------------- | --------------------------------------- | ---: |
| Order API            | Receives and exposes order-related APIs | 8000 |
| Order Processor      | Processes incoming orders               | 8000 |
| Notification Service | Handles order notifications             | 8000 |

All three services run on port `8000` inside their containers. Kubernetes provides separate Services for each application, so they can use the same internal port without conflict.

---

## Technology Stack

### Application

* Python
* FastAPI
* Uvicorn

### Containerization

* Docker
* Dockerfiles
* Python 3.12

### Kubernetes

* Kubernetes
* Minikube
* Kubernetes Deployments
* Kubernetes Services

### Kubernetes Packaging

* Helm

### CI/CD

* GitHub Actions
* Automated Python tests
* Pytest

### Infrastructure as Code

* Terraform
* Azure Resource Group
* Azure Container Registry
* Azure Kubernetes Service

---

## Project Structure

```text
order-processing-platform/
│
├── services/
│   ├── order-api/
│   │   ├── app/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── ...
│   │
│   ├── order-processor/
│   │   ├── app/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   ├── pytest.ini
│   │   ├── requirements.txt
│   │   └── ...
│   │
│   └── notification-service/
│       ├── app/
│       ├── tests/
│       ├── Dockerfile
│       ├── pytest.ini
│       ├── requirements.txt
│       └── ...
│
├── helm/
│   └── order-platform/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── deployment.yaml
│           └── service.yaml
│
├── terraform/
│   └── ...
│
├── .github/
│   └── workflows/
│       └── ...
│
└── README.md
```

---

# Prerequisites

For the local demonstration:

* Windows/Linux/macOS
* Python 3.12+
* Docker
* Docker Desktop
* Minikube
* kubectl
* Helm
* Git

For the Azure deployment:

* Azure subscription
* Azure CLI
* Terraform
* Azure Container Registry
* Azure Kubernetes Service

---

# 1. Clone the Repository

```bash
git clone https://github.com/manjarisri/order-processing-platform.git
cd order-processing-platform
```

---

# 2. Run Tests

Each service contains its own tests.

Example:

```bash
cd services/order-api
pytest
```

For the other services:

```bash
cd ../order-processor
pytest
```

```bash
cd ../notification-service
pytest
```

The GitHub Actions workflow automatically runs the tests for all three services.

---

# 3. Build Docker Images

Build the three application images:

```bash
docker build -t order-api:1.0.0 ./services/order-api
docker build -t order-processor:1.0.0 ./services/order-processor
docker build -t notification-service:1.0.0 ./services/notification-service
```

Verify the images:

```bash
docker images
```

Expected images:

```text
order-api:1.0.0
order-processor:1.0.0
notification-service:1.0.0
```

---

# 4. Start Minikube

Start the local Kubernetes cluster:

```bash
minikube start --driver=docker
```

Verify:

```bash
minikube status
```

Check the Kubernetes node:

```bash
kubectl get nodes
```

The node should be in `Ready` state.

---

# 5. Make Docker Images Available to Minikube

The application images need to be available inside the Minikube environment.

They can be loaded using:

```bash
minikube image load order-api:1.0.0
minikube image load order-processor:1.0.0
minikube image load notification-service:1.0.0
```

Verify:

```bash
minikube image ls
```

> If the images have already been built inside the Minikube Docker environment, this step may not be required.

---

# 6. Validate the Helm Chart

Run Helm lint:

```bash
helm lint ./helm/order-platform
```

Expected result:

```text
1 chart(s) linted, 0 chart(s) failed
```

To preview the generated Kubernetes manifests:

```bash
helm template order-platform ./helm/order-platform
```

---

# 7. Deploy Using Helm

Install the application:

```bash
helm upgrade --install order-platform ./helm/order-platform
```

Check the Helm release:

```bash
helm list
```

Expected status:

```text
deployed
```

---

# 8. Verify Kubernetes Resources

Check the pods:

```bash
kubectl get pods
```

Expected application pods:

```text
order-platform-order-api-...
order-platform-order-processor-...
order-platform-notification-service-...
```

Check Services:

```bash
kubectl get services
```

Check Deployments:

```bash
kubectl get deployments
```

All three application deployments should show `1/1` available.

---

# 9. Test Order API

Forward the Kubernetes Service to the local machine:

```bash
kubectl port-forward svc/order-platform-order-api 8001:8000
```

In another terminal:

```bash
curl http://localhost:8001/health
```

Expected response:

```json
{
  "status": "healthy",
  "service": "order-api"
}
```

FastAPI Swagger documentation is also available at:

```text
http://localhost:8001/docs
```

---

# 10. Test Order Processor

Forward the service:

```bash
kubectl port-forward svc/order-platform-order-processor 8002:8000
```

Health check:

```bash
curl http://localhost:8002/health
```

Process an order:

```powershell
curl -Method POST `
  -Uri http://localhost:8002/process `
  -ContentType "application/json" `
  -Body '{"order_id":"ORD-DEMO-001"}'
```

Expected response:

```json
{
  "order_id": "ORD-DEMO-001",
  "status": "PROCESSED"
}
```

---

# 11. Test Notification Service

Forward the service:

```bash
kubectl port-forward svc/order-platform-notification-service 8003:8000
```

Health check:

```bash
curl http://localhost:8003/health
```

Send a notification:

```powershell
curl -Method POST `
  -Uri http://localhost:8003/notify `
  -ContentType "application/json" `
  -Body '{"order_id":"ORD-DEMO-001"}'
```

Expected response:

```json
{
  "order_id": "ORD-DEMO-001",
  "status": "NOTIFICATION_SENT"
}
```

---

# 12. CI/CD with GitHub Actions

The project includes a GitHub Actions workflow that automatically validates the application.

The CI workflow performs tasks such as:

```text
Code Push
    |
    v
GitHub Actions
    |
    v
Install Dependencies
    |
    v
Run Tests
    |
    v
Validation
```

Tests are executed for:

* Order API
* Order Processor
* Notification Service

A successful workflow provides an automated quality gate before deployment.

---

# 13. Helm Configuration

The Helm chart uses `values.yaml` to configure the application.

Example:

```yaml
services:
  orderApi:
    name: order-api
    image:
      repository: order-api
      tag: "1.0.0"
    port: 8000
    replicas: 1
```

The same structure is used for the other services.

The chart also uses:

```yaml
imagePullPolicy: IfNotPresent
automountServiceAccountToken: false
resources: {}
```

This allows the local images to be used by Kubernetes without requiring a remote container registry.

---

# 14. Terraform and Azure Architecture

Terraform configuration is included for the intended Azure deployment architecture.

The target architecture is:

```text
Terraform
    |
    +---- Resource Group
    |
    +---- Azure Container Registry
    |
    +---- Azure Kubernetes Service
                 |
                 +---- Order API
                 |
                 +---- Order Processor
                 |
                 +---- Notification Service
```

Terraform allows the infrastructure to be defined as code and provisioned consistently.

---

# 15. Azure Deployment Note

The Azure architecture is included as the target cloud deployment model.

The complete application workflow was validated locally using:

```text
Docker
  ↓
Minikube
  ↓
Kubernetes
  ↓
Helm
```

An Azure subscription was not available during implementation, so the actual AKS/ACR deployment was not performed.

The Kubernetes and Helm deployment model is designed to be compatible with the intended AKS deployment.

---

# 16. DevOps Workflow

The complete workflow can be summarized as:

```text
Developer
    |
    v
GitHub
    |
    v
GitHub Actions
    |
    v
Automated Tests
    |
    v
Docker Images
    |
    v
Container Registry
    |
    v
Helm
    |
    v
Kubernetes / AKS
    |
    v
Running Application
```

For the local implementation, Minikube is used instead of AKS and local Docker images are used instead of ACR.

---

# 17. Cost Management Considerations

For an Azure deployment, important cost areas include:

* AKS compute resources
* Node pools
* Container Registry storage
* Networking
* Load balancers
* Monitoring and logging
* Persistent storage

Potential cost optimization practices include:

* Right-sizing resources
* Scaling workloads according to demand
* Removing unused resources
* Monitoring resource consumption
* Configuring budgets and alerts

---

# 18. Project Validation

The following parts of the implementation have been validated locally:

* FastAPI microservices
* Automated tests
* Docker image builds
* GitHub Actions CI
* Helm chart validation
* Kubernetes deployment
* Minikube cluster
* Kubernetes Services
* Order API health endpoint
* Order Processor API
* Notification Service API

---

# Key Takeaways

This project demonstrates how a microservices application can move through a modern DevOps workflow:

```text
Code
 ↓
Test
 ↓
Containerize
 ↓
CI
 ↓
Package with Helm
 ↓
Deploy to Kubernetes
 ↓
Validate Application
```

The same deployment model can be extended to Azure using:

```text
Terraform + ACR + AKS + Helm
```

---

## Future Enhancements

Possible future improvements include:

* Azure AKS deployment
* Azure Container Registry integration
* Kubernetes autoscaling
* Monitoring and observability
* Centralized logging
* Advanced security scanning
* Cloud cost monitoring

These are outside the scope of the current local demonstration.
