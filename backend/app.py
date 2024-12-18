from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from pyspark.sql import SparkSession
import graphene
from graphene import Argument, Field, Schema, List, String, Int, ObjectType
import logging
from utils.schema import SymptomAnalysis
from utils.parse_line import parse_line
from utils.clean_name import clean_disease_name

app = Flask(__name__)
CORS(app)  
logging.basicConfig(level=logging.INFO)

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("HDFS Reader") \
    .master("local[*]") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()

HDFS_PATH = 'hdfs://namenode:9000/data/out/symptom_analysis_count/part-r-00000'

class Query(ObjectType):
    analysis = Field(
        List(SymptomAnalysis),
        diseases=Argument(List(String)),
        symptoms=Argument(List(String)),
        outcome=Argument(String),
        min_count=Argument(Int)  # Changed from count to min_count
    )

    def resolve_analysis(self, info, diseases=None, symptoms=None, outcome=None, min_count=None):
        try:
            logging.info(f"Reading data from HDFS path: {HDFS_PATH}")
            logging.info(f"Received filters - diseases: {diseases}, symptoms: {symptoms}, "
                        f"outcome: {outcome}, min_count: {min_count}")
            
            rdd = spark.sparkContext.textFile(HDFS_PATH)
            processed_data = rdd.map(parse_line).filter(lambda x: x is not None).collect()
            
            # Apply filters sequentially
            filtered_data = processed_data

            # Apply disease filter
            if diseases:
                diseases = [clean_disease_name(disease) for disease in diseases]
                filtered_data = [
                    item for item in filtered_data 
                    if item['disease'] in diseases
                ]
                logging.info(f"After disease filter: {len(filtered_data)} items")
            
            # Apply symptoms filter
            if symptoms:
                filtered_data = [
                    item for item in filtered_data 
                    if any(symptom in item['symptoms'] for symptom in symptoms)
                ]
                logging.info(f"After symptoms filter: {len(filtered_data)} items")
            
            # Apply outcome filter
            if outcome:
                filtered_data = [
                    item for item in filtered_data 
                    if item['outcome'] == outcome
                ]
                logging.info(f"After outcome filter: {len(filtered_data)} items")
            
            # Apply minimum count filter
            if min_count is not None:
                filtered_data = [
                    item for item in filtered_data 
                    if item['count'] >= min_count
                ]
                logging.info(f"After min_count filter: {len(filtered_data)} items")
            
            # Sort by count in descending order
            filtered_data.sort(key=lambda x: x['count'], reverse=True)
            
            return [
                SymptomAnalysis(
                    disease=item['disease'],
                    symptoms=item['symptoms'],
                    outcome=item['outcome'],
                    count=item['count']
                ) for item in filtered_data
            ]
        
        except Exception as e:
            logging.error(f"Error in resolving GraphQL query: {e}")
            return []

schema = Schema(query=Query)

# Add GraphQL endpoint
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)