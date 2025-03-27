# Project Setup Guide

This guide will walk you through the process of setting up and running the project.

## Prerequisites
Before you begin, make sure you have the following installed on your machine:

- Python 3.9
- Docker (optional, for Docker setup)

## Setup Instructions

### 1. Activate Virtual Environment
First, create and activate a virtual environment to isolate the project’s dependencies.

#### On Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
Once your virtual environment is activated, install the required dependencies from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 3. Run the Project with Uvicorn
To start the application with Uvicorn and enable automatic reloading during development, run the following command:

```bash
uvicorn main:app --reload
```

This will start the FastAPI application, and you should be able to access it at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 4. Docker Setup (Optional)
If you want to use Docker to run the application, you can use the following commands:

#### Build and start the containers:
```bash
docker-compose up --build
```

This will build the Docker images and start the containers.

