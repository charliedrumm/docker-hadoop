from flask import Flask, jsonify
from pyspark.sql import SparkSession

app = Flask(__name__)

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("HDFS Reader") \
    .master("local[*]") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()


@app.route('/get-mapreduce-output', methods=['GET'])
def get_mapreduce_output():
    try:
        # Path to the MapReduce output file in HDFS
        hdfs_path = 'hdfs://namenode:9000/data/out/symptom_analysis_count/part-r-00000'
        
        # Read the file from HDFS
        rdd = spark.sparkContext.textFile(hdfs_path)
        
        # Collect data from RDD
        data = rdd.collect()
        
        return jsonify({
            'status': 'success',
            'message': 'Data retrieved from HDFS successfully',
            'data': data
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
