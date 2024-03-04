from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SearchableField,
    SemanticConfiguration,
    SimpleField,
    PrioritizedFields,
    SemanticField,
    SemanticSettings,
    VectorSearch,
    VectorSearchAlgorithmConfiguration,
)

def create_search_index(cognitive_search_index_name,cog_search_endpoint,cog_search_cred):
    index_name = cognitive_search_index_name

    # Create a search index and define the schema (names, types, and parameters)
    index_client = SearchIndexClient(
        endpoint=cog_search_endpoint, credential=cog_search_cred)
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String,
                        searchable=True, retrievable=True),
        SearchableField(name="type", type=SearchFieldDataType.String,
                        filterable=True, searchable=True, retrievable=True),
        SearchableField(name="tags", type=SearchFieldDataType.Collection(SearchFieldDataType.String),
                        filterable=True, searchable=True, retrievable=True),
        SearchField(name="contentVector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                    searchable=True, dimensions=1536, vector_search_configuration="my-vector-config"),
    ]

    # Configure vector search
    vector_search = VectorSearch(
        algorithm_configurations=[
            VectorSearchAlgorithmConfiguration(
                name="my-vector-config",
                kind="hnsw",
                hnsw_parameters={
                    "m": 4,
                    "efConstruction": 400,
                    "efSearch": 1000,
                    "metric": "cosine"
                }
            )
        ]
    )

    # Configure semantic search. This will allow us to conduct semantic or hybrid search (with vector search) later on if desired.
    semantic_config = SemanticConfiguration(
        name="my-semantic-config",
        prioritized_fields=PrioritizedFields(
            prioritized_keywords_fields=[SemanticField(field_name="type")],
            prioritized_content_fields=[SemanticField(field_name="content")]
        )
    )

    # Create the semantic settings with the configuration
    semantic_settings = SemanticSettings(configurations=[semantic_config])

    # Create the search index with the semantic settings
    index = SearchIndex(name=index_name, fields=fields,
                        vector_search=vector_search, semantic_settings=semantic_settings)
    result = index_client.create_or_update_index(index)
    print(f' {result.name} created')
