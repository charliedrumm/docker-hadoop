#!/bin/bash

# Format hdfs
hdfs namenode -format -force -nonInteractive
hdfs namenode & sleep 10

until hdfs dfs -ls /; do
  sleep 5
done

# Create directories and set permissions 
hdfs dfs -mkdir -p /data/in/
hdfs dfs -chmod -R 777 /data

# Copy data to HDFS
hdfs dfs -put /opt/hadoop/data/* /data/in/

hadoop jar mapreduce-jobs/target/hadoop-mapreduce-examples-2.7.1-sources.jar org.apache.hadoop.examples.WordCount /data/in/simplified_disease_symptom.txt /data/out/symptom_analysis_count

# Stop container from quitting
tail -f /dev/null