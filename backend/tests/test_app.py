import pytest
from unittest.mock import Mock, patch
from flask import json
from app import app, spark, HDFS_PATH

# Sample test data that mimics HDFS output
MOCK_HDFS_DATA = [
    "COVID-19_Fever_Cough_Positive\t4",
    "Asthma_DifficultyBreathing_Negative\t1",
    "Diabetes_Fatigue_Fever_Positive\t2"
]

# Mock processed data after parse_line transformation
MOCK_PROCESSED_DATA = [
    {
        'disease': 'COVID-19',
        'symptoms': ['Fever', 'Cough'],
        'outcome': 'Positive',
        'count': 4
    },
    {
        'disease': 'Asthma',
        'symptoms': ['DifficultyBreathing'],
        'outcome': 'Negative',
        'count': 1
    },
    {
        'disease': 'Diabetes',
        'symptoms': ['Fatigue', 'Fever'],
        'outcome': 'Positive',
        'count': 2
    }
]

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_spark_context():
    # Create mock RDD
    mock_rdd = Mock()
    
    # Configure the mock RDD's behavior
    def mock_map(func):
        # Apply the actual transformation function to our mock data
        transformed_data = [func(line) for line in MOCK_HDFS_DATA]
        mock_rdd.collect.return_value = transformed_data
        return mock_rdd
    
    mock_rdd.map = mock_map
    mock_rdd.filter = lambda x: mock_rdd  # Return self for chaining
    mock_rdd.collect.return_value = MOCK_PROCESSED_DATA

    # Patch spark.sparkContext.textFile
    with patch.object(spark.sparkContext, 'textFile', return_value=mock_rdd):
        yield

def test_get_mapreduce_output_success(client, mock_spark_context):
    response = client.get('/get-mapreduce-output')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert len(data['data']) == 3
    
    first_entry = data['data'][0]
    assert first_entry['disease'] == 'COVID-19'
    assert 'Fever' in first_entry['symptoms']
    assert 'Cough' in first_entry['symptoms']
    assert first_entry['outcome'] == 'Positive'
    assert first_entry['count'] == 4

def test_graphql_query_all(client, mock_spark_context):
    query = """
    {
        analysis {
            disease
            symptoms
            outcome
            count
        }
    }
    """
    
    response = client.post('/graphql', 
                          json={'query': query})
    data = json.loads(response.data)
    
    assert 'errors' not in data
    assert 'data' in data
    assert 'analysis' in data['data']
    assert len(data['data']['analysis']) == 3
    
    first_entry = data['data']['analysis'][0]
    assert first_entry['disease'] == 'COVID-19'
    assert 'Fever' in first_entry['symptoms']
    assert first_entry['outcome'] == 'Positive'

def test_graphql_query_filtered(client, mock_spark_context):
    query = """
    {
        analysis(disease: "COVID-19") {
            disease
            symptoms
            outcome
            count
        }
    }
    """
    
    response = client.post('/graphql', 
                          json={'query': query})
    data = json.loads(response.data)
    
    assert 'errors' not in data
    assert 'data' in data
    assert 'analysis' in data['data']
    assert len(data['data']['analysis']) == 1
    assert data['data']['analysis'][0]['disease'] == 'COVID-19'

def test_get_mapreduce_output_error(client):
    with patch.object(spark.sparkContext, 'textFile', side_effect=Exception('HDFS Error')):
        response = client.get('/get-mapreduce-output')
        data = json.loads(response.data)
        
        assert response.status_code == 500
        assert data['status'] == 'error'
        assert 'HDFS Error' in data['message']

def test_graphql_error_handling(client):
    with patch.object(spark.sparkContext, 'textFile', side_effect=Exception('HDFS Error')):
        query = """
        {
            analysis {
                disease
                symptoms
                outcome
                count
            }
        }
        """
        
        response = client.post('/graphql', 
                             json={'query': query})
        data = json.loads(response.data)
        
        assert 'data' in data
        assert data['data']['analysis'] == []