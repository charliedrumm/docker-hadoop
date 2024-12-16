#!/bin/bash

# Format hdfs
hdfs namenode -format -force -nonInteractive
hdfs namenode & sleep 5

# Create directories and set permissions 
hadoop fs -mkdir -p /data/in/
hadoop fs -chmod -R 777 /data

# Copy data to HDFS
hadoop fs -put /opt/hadoop/data/* /data/in/

hadoop jar mapreduce-jobs/target/hadoop-mapreduce-examples-2.7.1-sources.jar org.apache.hadoop.examples.WordCount /data/in/simplified_disease_symptom.txt /data/out/symptom_analysis_count


# Stop container from quitting
tail -f /dev/null