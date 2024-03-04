from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndexer,
    SearchIndexerDataContainer,
    SearchIndexerDataSourceConnection
)


def _create_datasource(cog_search_endpoint,cog_search_cred,cosmos_db_container_id,cognitive_search_indexer_name,cosmosdb_connection_str):
    # Here we create a datasource. 
    ds_client = SearchIndexerClient(cog_search_endpoint, cog_search_cred)
    container = SearchIndexerDataContainer(name=cosmos_db_container_id)
    data_source_connection = SearchIndexerDataSourceConnection(
        name=cognitive_search_indexer_name, type="cosmosdb", connection_string=cosmosdb_connection_str, container=container
    )
    data_source = ds_client.create_or_update_data_source_connection(data_source_connection)
    return data_source

def run_search_indexer(cognitive_search_indexer_name,cognitive_search_index_name,cog_search_endpoint,cog_search_cred,cosmos_db_container_id,cosmosdb_connection_str):

    index_name = cognitive_search_index_name

    ds_name = _create_datasource(cog_search_endpoint,cog_search_cred,cosmos_db_container_id,cognitive_search_indexer_name,cosmosdb_connection_str).name

    # Define indexer
    indexer = SearchIndexer(
            name=cognitive_search_indexer_name,
            data_source_name=ds_name,
            target_index_name=index_name)

    # Create indexer client
    indexer_client = SearchIndexerClient(cog_search_endpoint, cog_search_cred)

    # Create indexer
    indexer_client.create_or_update_indexer(indexer)

    result = indexer_client.get_indexer(cognitive_search_indexer_name)
    print("Created indexer")

    # Run the indexer we just created to ingest data into the search index.
    indexer_client.run_indexer(result.name)
