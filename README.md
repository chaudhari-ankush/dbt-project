# DBT + FastAPI Dockerized Project

This project demonstrates how to integrate [DBT Core](https://www.getdbt.com/) with [FastAPI](https://fastapi.tiangolo.com/) in a Docker container, deployable to AWS ECS. It exposes a REST API to run a sample DBT model.

## Features
- DBT Core for analytics engineering
- FastAPI for RESTful API
- Dockerized for easy deployment
- ECS-ready
- Sample DBT model execution via API

## Structure
- `app/` - FastAPI application
- `dbt/` - DBT project (models, profiles, etc.)
- `Dockerfile` - Container build
- `requirements.txt` - Python dependencies
- `ecs/` - ECS deployment configuration

## Usage
1. Build Docker image
2. Run locally or deploy to ECS
3. Use REST API to trigger DBT models 