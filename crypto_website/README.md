# Django Docker Setup with PostgreSQL

This repository contains a simple setup for running a Django application with PostgreSQL inside Docker containers. The setup leverages Docker Compose to run both the Django application and PostgreSQL database. The Django application is served using the default development server (not Gunicorn).

## Prerequisites

Make sure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Project Structure

- `docker-compose.yml`: Defines the services, including the web and database containers.
- `Dockerfile`: Specifies how to build the Docker image for the Django app.
- `entrypoint.sh`: A script used to run migrations and start the Django development server.
- `wait-for-it.sh`: A script to ensure the database is available before starting the Django app.
- `myproject/`: The main Django project directory.
- `requirements.txt`: Lists the Python dependencies for the project.

## Getting Started

### 1. Clone the repository

Start by cloning this repository:

```bash
git clone git@github.com:osieks/python_exchanges_Django_website.git
cd python_exchanges_Django_website
docker compose up --build -d
