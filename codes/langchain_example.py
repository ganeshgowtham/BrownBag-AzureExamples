from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.llms.openai import OpenAI
from langchain.chains.summarize import load_summarize_chain

# Get OpenAI API key and source text input
openai_api_key = "<paste openai_api_key>"
source_text = "<paste source_text>"

try:
    # Split the source text
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(source_text)

    # Create Document objects for the texts
    docs = [Document(page_content=t) for t in texts[:3]]

    # Initialize the OpenAI module, load and run the summarize chain
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(docs)

    # Display summary
    print(summary)
except Exception as e:
    print(f"An error occurred: {e}")