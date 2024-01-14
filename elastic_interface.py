import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json

class Elastic:
    def __init__(self):
        # Elasticsearch connection settings
        self.es_user = 'elastic'
        self.es_password = 'mfb6RIIrWNrg7ors2LhA'

        # Create Elasticsearch connection with authentication
        self.es = Elasticsearch(
            "https://localhost:9200",
            http_auth=[self.es_user,self.es_password],
            verify_certs=False
        )
        # Specify your index (without doc_type for recent Elasticsearch versions)
        self.index_name = 'stocks'
    
    def load_data(self):
        # Read CSV file into a DataFrame
        csv_file_path = 'EQUITY_L.csv'
        df = pd.read_csv(csv_file_path)

        # Convert DataFrame to JSON with orient='records'
        json_data = df.to_json(orient='records')

        # Convert JSON data to a list of dictionaries
        documents = json.loads(json_data)

        # Use the bulk API to index the data
        actions = [
            {"_op_type": "index", "_index": self.index_name, "_source": doc}
            for doc in documents
        ]

        success, failed = bulk(self.es, actions)

        print(f"Successfully indexed {success} documents. Failed to index {failed} documents.")
    
    def perform_search(self,search_term):
        if not search_term:
            return
        print(search_term)
        q = {
            "query": {
		        "match" : {
			        "NAME OF COMPANY": {
				        "query": search_term,
				        "fuzziness": "AUTO"
			                }
		                }
	                }
            }
        search_results = self.es.search(index=self.index_name, body=q)
       
        for hit in search_results['hits']['hits']:
            return hit['_source']['Symbol']

elastic = Elastic()
#elastic.load_data()
#print(elastic.perform_search("Boeing"))