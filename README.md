# FastAPI DBT Integration with AWS ECS Fargate

This project integrates FastAPI with dbt core, containerized using Docker and deployable to AWS ECS Fargate.

## Project Structure
```
.
├── app/
│   └── main.py
├── models/
│   └── example_model.sql
├── analyses/
├── tests/
├── seeds/
├── macros/
├── snapshots/
├── Dockerfile
├── dbt_project.yml
├── profiles.yml
├── task-definition.json
├── requirements.txt
└── README.md
```

## Local Development

1. Create a `.env` file with your database credentials:
```bash
DB_HOST=your-db-host
DB_PORT=5432
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_NAME=your-db-name
```

2. Build the Docker image:
```bash
docker build -t fastapi-dbt .
```

3. Run the container:
```bash
docker run -p 8000:8000 --env-file .env fastapi-dbt
```

## AWS ECS Fargate Deployment

1. Create an ECR repository:
```bash
aws ecr create-repository --repository-name fastapi-dbt
```

2. Authenticate Docker to ECR:
```bash
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com
```

3. Tag and push the image:
```bash
docker tag fastapi-dbt:latest <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/fastapi-dbt:latest
docker push <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/fastapi-dbt:latest
```

4. Store database password in AWS Systems Manager Parameter Store:
```bash
aws ssm put-parameter \
    --name "/dbt/db-password" \
    --value "your-db-password" \
    --type SecureString
```

5. Create an ECS cluster:
```bash
aws ecs create-cluster --cluster-name fastapi-dbt-cluster
```

6. Register the task definition:
```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

7. Create a service:
```bash
aws ecs create-service \
    --cluster fastapi-dbt-cluster \
    --service-name fastapi-dbt-service \
    --task-definition fastapi-dbt \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}"
```

## API Endpoints

- GET `/`: Health check endpoint
- GET `/health`: Detailed health check with configuration validation
- POST `/run-dbt`: Trigger dbt run
- GET `/dbt-docs`: Generate dbt documentation

## Notes

- The application runs on port 8000
- Make sure to update the task-definition.json with your specific values
- Ensure proper AWS IAM roles and permissions are set up for ECS deployment
- The example model generates sample data using PostgreSQL's generate_series function
- Database credentials are stored securely in AWS Systems Manager Parameter Store
- The Fargate task is configured with 256 CPU units (0.25 vCPU) and 512MB memory 

# DBT Project Structure

This project follows the standard DBT structure:

- `models/`: Your DBT models (SQL files that build tables/views)
- `analyses/`: (Optional) For ad-hoc analysis SQL files
- `tests/`: (Optional) For custom data tests
- `seeds/`: (Optional) For CSV files to load static data
- `macros/`: (Optional) For custom Jinja macros
- `snapshots/`: (Optional) For snapshotting slowly changing data
- `dbt_project.yml`: Main project config
- `profiles.yml`: Database connection config (usually in ~/.dbt/) 