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

This command will spin up the Hadoop services (Namenode, Datanode, etc.).

### 3. Copy Data and JAR File to Namenode

Copy the MapReduce examples JAR and the dataset to the Namenode container:

```sh
docker cp hadoop-mapreduce-examples-2.7.1-sources.jar namenode:/tmp
docker cp data/simplified_disease_symptom.txt namenode:/root/simplified_disease_symptom.txt
```

### 4. Run Hadoop Commands on Namenode

Execute an interactive bash session on the Namenode container:

```sh
docker exec -it namenode bash
```

Run the following commands:

1. Create an input directory in HDFS and put the dataset into it:

   ```sh
   hdfs dfs -mkdir -p /input
   hdfs dfs -put /root/simplified_disease_symptom.txt /input/
   ```

2. Run Word Count Example:

   ```sh
   cd tmp
   hadoop jar hadoop-mapreduce-examples-2.7.1-sources.jar org.apache.hadoop.examples.WordCount /input/simplified_disease_symptom.txt output/symptom_analysis_count
   ```

3. Run Custom Symptom-Disease Analysis Job:

   ```sh
   hadoop jar symptom-disease-analysis.jar diseasymptomanalysis.SymptomDiseaseAnalysis /input/simplified_disease_symptom.txt /output/symptom_analysis_output
   ```

4. View the Word Count Output:

   ```sh
   hdfs dfs -cat /user/root/output/symptom_analysis_count/*
   ```

5. Copy the Word Count output from HDFS to the local filesystem:
   ```sh
   hdfs dfs -get /user/root/output/symptom_analysis_count/part-r-00000 symptom_analysis_count.txt
   ```

### 5. Copy Output File to Local Machine

Exit the namenode container and copy the output file to your local machine:

```sh
docker cp namenode:/tmp/symptom_analysis_count.txt "C:\Users\User\Desktop\Charlie College\Cloud\Projects\P3\hdfs-docker-compose-main\cloud_project\docker-hadoop\backend"
```

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
