from azure.cosmos import exceptions, CosmosClient, PartitionKey

cosmosdb_endpoint = "<paste cosmos_db_api_endpoint>"
cosmosdb_key = "<paste cosmos_db_api_key>"
cosmosdb_connection_str = "<paste cosmos_db_connection_string>"
cosmos_db_container_id = "<paste cosmos_db_container_id>"
cosmos_db_id = "<paste cosmos_db_id>"


# Create the cosmos client to interact with the Azure Cosmos DB resource
client = CosmosClient(cosmosdb_endpoint, cosmosdb_key)

# Create a database in Azure Cosmos DB.
try:
    database = client.create_database_if_not_exists(id=cosmos_db_id)
    print(f"Database created: {database.id}")

except exceptions.CosmosResourceExistsError:
    print("Database already exists.")

# Create a container in Azure Cosmos DB.
try:
    partition_key_path = PartitionKey(path="/id")
    container = database.create_container_if_not_exists(
        id=cosmos_db_container_id,
        partition_key=partition_key_path,
        offer_throughput=400,
    )
    print(f"Container created: {container.id}") 

except exceptions.CosmosResourceExistsError:
    print("Container already exists.")


# Ingest embedded data into Cosmos DB container
data = []

for item in data:
    try:
        container.create_item(body=item)
    
    except exceptions.CosmosResourceExistsError:
        print("Data item already exists.")