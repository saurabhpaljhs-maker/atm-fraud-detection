# Real-Time ATM Fraud Detection Pipeline

## Overview

A production-grade fraud detection system that processes ATM transactions in real-time using Google Cloud Platform and Azure DevOps. The system ingests transaction streams, applies fraud detection rules, and stores results in BigQuery for analytics.

## Architecture

flowchart LR
    subgraph "Source Control & CI/CD"
        GitHub[GitHub Repo] 
        AzDO[Azure DevOps] 
    end

    subgraph "Infrastructure as Code"
        Terraform[Terraform IaC] 
    end

    subgraph "Google Cloud Platform"
        GKE[GKE Cluster<br/>atm-fraud-gke]
        PubSub[Pub/Sub Topic & Subscription]
        BQ[BigQuery Dataset & Table]
        Artifact[Artifact Registry]
    end

    subgraph "Application Components"
        Producer[Producer.py<br/>Transaction Generator]
        Consumer[Consumer.py + fraud_detector.py<br/>Real-time Processor]
    end

    %% CI/CD Flow
    GitHub --> AzDO
    AzDO --> Docker[Docker Build & Push]
    Docker --> Artifact

    %% Infrastructure
    Terraform --> GKE
    Terraform --> PubSub
    Terraform --> BQ

    %% Data Flow
    Producer --> PubSub
    PubSub --> Consumer
    Consumer --> BQ
    Consumer -. Fraud Alert .-> Monitoring[Real-time Alerts]

    classDef gcp fill:#4285F4,stroke:#fff,stroke-width:2px,color:white;
    classDef tool fill:#34A853,stroke:#fff,stroke-width:2px,color:white;
    classDef app fill:#FBBC05,stroke:#333,stroke-width:2px;

    class GKE,PubSub,BQ,Artifact gcp
    class Terraform,AzDO,Docker tool
    class Producer,Consumer app

**Producer Component**
- Generates simulated ATM transactions with realistic data (card ID, amount, location, timestamp)
- Publishes messages to Google Cloud Pub/Sub topic
- Simulates real-world transaction volume (~1 transaction every 2 seconds)

**Consumer Component**
- Subscribes to Pub/Sub topic for real-time message consumption
- Applies multi-factor fraud detection logic
- Stores transaction records and fraud flags in BigQuery
- Provides real-time fraud alerts

**Fraud Detection Logic**
- Velocity analysis: Detects multiple transactions from same card within 5-minute window
- Geographic anomalies: Flags transactions from same card across different locations within 2 minutes
- Amount threshold: Identifies transactions exceeding ₹25,000 limit

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11 |
| Cloud Platform | Google Cloud Platform (GCP) |
| Message Queue | Pub/Sub |
| Data Warehouse | BigQuery |
| Container Runtime | Docker |
| Orchestration | Kubernetes (GKE) |
| Infrastructure as Code | Terraform |
| CI/CD Pipeline | Azure DevOps |

## Project Metrics

- **Transactions Processed**: 247+
- **Fraud Detected**: 44 (17.8% fraud rate)
- **Real-time Processing**: Verified ✓
- **Data Storage**: BigQuery ✓
- **Container Image**: Successfully built and tested ✓

## Deployment

### Prerequisites
- Google Cloud Project with billing enabled
- Terraform installed locally
- Docker installed locally
- Azure DevOps organization and project

### Infrastructure Setup
```bash
cd terraform/
terraform init
terraform plan
terraform apply
```

This creates:
- GKE cluster (atm-fraud-gke)
- Artifact Registry repository
- Pub/Sub topic and subscription
- BigQuery dataset and table

### Local Testing
```bash
pip install -r requirements.txt
export GOOGLE_CLOUD_PROJECT=atm-fraud-detection

# Terminal 1: Run Producer
python3 producer.py

# Terminal 2: Run Consumer
python3 consumer.py
```

### Docker Build
```bash
docker build -t atm-fraud-consumer:1.0 .
docker run --rm -e GOOGLE_CLOUD_PROJECT=atm-fraud-detection atm-fraud-consumer:1.0
```

### CI/CD Pipeline
Azure DevOps pipeline automatically:
1. Validates Python syntax
2. Packages application
3. Creates deployment artifacts
4. Verifies deployment readiness

## Project Structure

atm-fraud-detection/

├── producer.py              # Transaction generator

├── consumer.py              # Real-time processor

├── fraud_detector.py        # Detection logic

├── requirements.txt         # Python dependencies

├── Dockerfile              # Container image definition

├── terraform/

│   ├── main.tf            # GCP resource definitions

│   └── variables.tf       # Variable declarations

├── kubernetes/

│   ├── producer-deployment.yaml

│   └── consumer-deployment.yaml

├── azure-pipelines.yml    # CI/CD configuration

└── README.md

## Key Features

- **Real-time Processing**: Sub-second latency from transaction ingestion to fraud detection
- **Scalable Architecture**: Kubernetes-based deployment supports automatic scaling
- **Infrastructure as Code**: Terraform ensures reproducible deployments
- **Automated CI/CD**: Azure DevOps pipeline handles build, test, and deployment
- **Production-Ready**: Follows industry best practices for security and monitoring

## Experience Applied

This project demonstrates real-world banking domain knowledge from previous experience with NCR Voyix ATM systems, combined with modern cloud-native DevOps practices. The implementation covers end-to-end system design from data ingestion through fraud detection to deployment orchestration.

## Author

Saurabh Pal  
Multi-Cloud DevOps Engineer  
[Portfolio](https://saurabhpalportfolio.netlify.app) 
