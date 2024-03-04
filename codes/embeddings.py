from langchain.embeddings import HuggingFaceEmbeddings

embeddings_model_name = "all-MiniLM-L6-v2"

embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

v1 = [embeddings.embed_query("Wires is a type of payment")]

print(v1)