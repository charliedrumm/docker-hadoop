# Symptom Disease Analysis using Hadoop & Flask

This project analyzes disease symptoms using Hadoop MapReduce and presents the results through a Flask-based web interface. Below is a step-by-step guide to set up and run the project.

## Prerequisites

- Docker & Docker Compose
- Python 3.x
- Java 1.8

## Directory Structure

- `data/`: Contains data files to be processed.
- `backend/`: Contains the Flask server files for presenting the analysis.
- `docker-hadoop/`: Contains the Docker Compose setup for the Hadoop environment.

## Steps to Run the Project

### 1. Clean and Set Up Data Directory

Ensure that the `data` directory is clean and has the required dataset file (`simplified_disease_symptom.txt`).

### 2. Start Hadoop Services with Docker Compose

Navigate to the project root and run:

```sh
docker compose up
```

data should be mapped and reduced in hdfs dfs -cat /data/out/symptom_analysis_count/part-r-00000

### 6. Set Up Backend Flask Server

Navigate to the `backend` directory:

```sh
cd backend
```

Create a virtual environment and install dependencies:

```sh
python -m venv venv
venv\Scripts\activate
pip install flask pandas matplotlib
```

### 7. Run Flask Application

Run the Flask server to present the analysis results:

```sh
python app.py
```

The server will start, and you can view the output in your browser at `http://localhost:5000`.

## Conclusion

Follow these steps to successfully run the symptom-disease analysis using Hadoop and Flask. This setup will allow users to gain insights into the relationships between diseases and symptoms.
