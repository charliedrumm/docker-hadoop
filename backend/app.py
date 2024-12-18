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
        
        # Transform each line into a key-value pair
        # Each line is in format "Disease_Symptoms_Outcome    Count"
        transformed_rdd = rdd.map(lambda line: {
            "key": line.split('\t')[0],  # Everything before the tab
            "count": int(line.split('\t')[1])  # The count after the tab
        })
        
        # Collect data from RDD
        data = transformed_rdd.collect()
        
        # Further process each entry to split disease and symptoms
        processed_data = []
        for item in data:
            parts = item['key'].split('_')
            entry = {
                'disease': parts[0],
                'symptoms': parts[1:-1] if len(parts) > 2 else [],
                'outcome': parts[-1] if len(parts) > 1 else None,
                'count': item['count']
            }
            processed_data.append(entry)
        
        return jsonify({
            'status': 'success',
            'message': 'Data retrieved and processed from HDFS successfully',
            'data': processed_data
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
