from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import Vector
from azure.search.documents import SearchClient
import openai

from azure_search_index import create_search_index
from azure_search_indexer import run_search_indexer

cog_search_endpoint = "<paste cognitive_search_api_endpoint>"
cog_search_key = "<paste cognitive_search_api_key>"
cognitive_search_index_name = "<paste cognitive_search_index_name>"
cognitive_search_indexer_name = "<paste cognitive_search_indexer_name>"

cosmosdb_connection_str = "<paste cosmos_db_connection_string>"
cosmos_db_container_id = "<paste cosmos_db_container_id>"

embeddings_deployment = "<paste openai_embeddings_deployment>"

# Create index

cog_search_cred = AzureKeyCredential(cog_search_key)

create_search_index(cognitive_search_index_name,cog_search_endpoint,cog_search_cred)
run_search_indexer(cognitive_search_indexer_name,cognitive_search_index_name,cog_search_endpoint,cog_search_cred,cosmos_db_container_id,cosmosdb_connection_str)

def generate_embeddings(text):
    response = openai.Embedding.create(
        input=text, engine=embeddings_deployment)
    embeddings = response['data'][0]['embedding']
    return embeddings

# Function to assist with vector search
def vector_search(query):
    search_client = SearchClient(cog_search_endpoint, cognitive_search_index_name, cog_search_cred)  
    results = search_client.search(  
        search_text="",  
        vector=Vector(value=generate_embeddings(query), k=3, fields="contentVector"),  
        select=["content", "type", "tags"] 
    )
    return results

query = "<paste query>"  
results = vector_search(query)
for result in results:
    print(f"Title: {result['tags']}")  
    print(f"Score: {result['@search.score']}")  
    print(f"Content: {result['content']}")  
    print(f"Category: {result['type']}\n") 