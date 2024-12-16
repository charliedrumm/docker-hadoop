#!/bin/bash

# Start Hadoop services
echo "Starting Hadoop services..."
/etc/bootstrap.sh -d

# Wait for Hadoop to start
sleep 20

# Create HDFS directory to store the CSV file
echo "Creating directory in HDFS for CSV file..."
hdfs dfs -mkdir -p /user/raw_data

# Upload the CSV file into HDFS
echo "Uploading Disease_symptom_dataset.csv to HDFS..."
hdfs dfs -put -f /data/simplified_disease_symptom.txt /user/raw_data/

# Verify if the file is uploaded
echo "Verifying that the file is in HDFS..."
hdfs dfs -ls /user/raw_data/

# Run the MapReduce job
echo "Running the WordCount MapReduce job..."
hadoop jar /reduce_jobs/target/hadoop-mapreduce-examples-2.7.1-sources.jar org.apache.hadoop.examples.WordCount /user/raw_data/simplified_disease_symptom.txt /user/output/symptom_analysis_count

# Verify the MapReduce output
echo "Verifying the MapReduce output..."
hdfs dfs -ls /user/project_name/output/symptom_analysis_count

# Keep the container running
tail -f /dev/null
