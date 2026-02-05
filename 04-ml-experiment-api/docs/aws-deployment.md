# AWS Deployment Guide

Guide for deploying the ML Experiment API to AWS.

## Prerequisites

- AWS Account
- AWS CLI installed and configured
- Docker installed locally
- Basic AWS knowledge

## Setup AWS CLI

```bash
# Install AWS CLI (macOS)
brew install awscli

# Configure credentials
aws configure
# Enter: Access Key ID, Secret Access Key, Region (e.g., eu-central-1), Output format (json)

# Verify
aws sts get-caller-identity
```

## Option 1: Deploy to EC2

Suitable for learning and cost-effective small-scale deployments.

**Step 1: Launch EC2 Instance**

```bash
# Launch Ubuntu instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.small \
  --key-name your-key-pair \
  --security-group-ids sg-xxxxxxxxx \
  --subnet-id subnet-xxxxxxxxx \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=ml-api-server}]'
```

Or use AWS Console:
1. Navigate to EC2 → Launch Instance
2. Choose Ubuntu 22.04 LTS
3. EC2 → Launch Instance
2. Ubuntu 22.04 LTS
3. Instance type: t3.small (2 vCPU, 2GB RAM)
4. Create or select key pair for SSH
5. Security group: Allow ports 22 (SSH), 8000 (API)

**Step 2: Connect and Setup**
# SSH into instance
ssh -i your-key.pem ubuntu@<instance-public-ip>

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# Logout and login again for docker group to take effect
exit
ssh -i your-key.pem ubuntu@<instance-public-ip>
```

### Step 3: Deploy Application

**Step 3: Deploy Application**
# Clone repository (or copy files via SCP)
git clone https://github.com/ozlem-senel/ml-systems-portfolio.git
cd ml-systems-portfolio/04-ml-experiment-api

# Build Docker image
docker build -t ml-api:latest -f docker/Dockerfile .

# Run container
docker run -d \
  --name ml-api \
  --restart unless-stopped \
  -p 8000:8000 \
  ml-api:latest

# Check logs
docker logs ml-api

# Verify
curl http://localhost:8000/health
```

### Step 4: Access API

**Step 4: Access API**

API is now available at: `http://<instance-public-ip>:8000`

Cost: ~$15/month (t3.small)

## Option 2: Deploy to ECS with Fargate

For production-like scalable infrastructure.

**Step 1: Create ECR Repository**

```bash
# Create repository for Docker images
aws ecr create-repository --repository-name ml-api

# Get repository URI
aws ecr describe-repositories --repository-names ml-api
```

**Step 2: Push Docker Image to ECR**

```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region eu-central-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.eu-central-1.amazonaws.com

# Build and tag image
cd 04-ml-experiment-api
docker build -t ml-api:latest -f docker/Dockerfile .
docker tag ml-api:latest <account-id>.dkr.ecr.eu-central-1.amazonaws.com/ml-api:latest

# Push to ECR
docker push <account-id>.dkr.ecr.eu-central-1.amazonaws.com/ml-api:latest
```

**Step 3: Create ECS Cluster**

```bash
# Create cluster
aws ecs create-cluster --cluster-name ml-api-cluster
```

Or via Console:
1. ECS → Clusters → Create Cluster
2. Choose "Networking only" (Fargate)
3. Cluster name: ml-api-cluster

**Step 4: Create Task Definition**

Create `task-definition.json`:

```json
{
  "family": "ml-api-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "ml-api",
      "image": "<account-id>.dkr.ecr.eu-central-1.amazonaws.com/ml-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ml-api",
          "awslogs-region": "eu-central-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

Register task:
```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

**Step 5: Create Service**

```bash
aws ecs create-service \
  --cluster ml-api-cluster \
  --service-name ml-api-service \
  --task-definition ml-api-task \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

**Step 6 (Optional): Add Load Balancer**

For production:
1. Create target group (type: IP, port 8000)
2. Create ALB
3. Update ECS service to use load balancer

Cost: ~$30-50/month (Fargate + ALB)

## Option 3: Use S3 for Model Storage

**Step 1: Create S3 Bucket**

```bash
aws s3 mb s3://ml-api-models-<unique-id>
```

### Step 2: Upload Models

```bash
aws s3 cp models/churn_model.pkl s3://ml-api-models-<unique-id>/models/churn_model.pkl
```

### Step 3: Update API Code

```python
import boto3

s3 = boto3.client('s3')
bucket = 'ml-api-models-<unique-id>'

# Download model on startup
s3.download_file(bucket, 'models/churn_model.pkl', '/tmp/churn_model.pkl')

# Load model
model = joblib.load('/tmp/churn_model.pkl')
```

**Step 4: Grant ECS Task S3 Access**

Create IAM role with S3 read permissions and attach to ECS task.

Cost: ~$0.50/month for storage

## Monitoring & Logging

**CloudWatch Logs**

Container logs go to CloudWatch when configured in task definition.

View logs:
```bash
aws logs tail /ecs/ml-api --follow
```

**CloudWatch Alarms**

Set up alarms for:
- High CPU usage
- Memory usage
- API error rates

## Cost Summary

| Option | Monthly Cost | Use Case |
|--------|--------------|----------|
| EC2 t3.small | ~$15 | Learning, development |
| ECS Fargate (1 task) | ~$30 | Production, scalable |
| ECS + ALB | ~$50 | High availability |
| S3 storage | ~$0.50 | Model artifacts |

## Security Best Practices

1. Never commit AWS credentials - use environment variables or IAM roles
2. Use Security Groups to restrict access to necessary ports only
3. Use HTTPS with ALB and SSL certificate from AWS Certificate Manager
4. Grant minimum necessary permissions with IAM Roles
5. Use AWS Secrets Manager for API keys

## Troubleshooting

## Troubleshooting

**API not responding:**
```bash
# Check if container is running
docker ps

# View logs
docker logs ml-api

# On ECS, check task status
aws ecs describe-tasks --cluster ml-api-cluster --tasks <task-id>
```

**Out of memory:**
- Increase task memory in task definition
- Optimize model loading with lazy loading or quantization

**Slow cold starts:**
- Keep at least 1 task running
- Use smaller base images like Alpine

## Next Steps

- Set up CI/CD with GitHub Actions
- Add API authentication
- Configure auto-scaling
- Set up custom domain with Route 53
- Implement blue-green deployment
