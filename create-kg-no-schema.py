import asyncio
import neo4j
import os
from dotenv import load_dotenv
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from neo4j_graphrag.experimental.components.text_splitters.fixed_size_splitter import FixedSizeSplitter

# This example requires adding OPENAI_API_KEY, and Neo4j connection details to .env file
load_dotenv()

# Neo4j connection details
NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.getenv('NEO4J_USERNAME', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD',"password")
AUTH = (NEO4J_USER, NEO4J_PASSWORD)

# Initialize the Neo4j driver 
driver = neo4j.GraphDatabase.driver(NEO4J_URI, auth=AUTH)

# Create the embedder instance
embedder = OpenAIEmbeddings()

# Create the llm instance - This example requires an OPENAI_API_KEY env variable
llm = OpenAILLM(
        model_name="gpt-4o",
        model_params={
            "max_tokens": 2000,
            "response_format": {"type": "json_object"},
            "temperature": 0,
        },
)

# Create a SimpleKGPipeline instance without providing a schema - This will trigger automatic schema extraction
kg_builder = SimpleKGPipeline(
    llm=llm,
    driver=driver,
    embedder=embedder,
    from_pdf=True,
    text_splitter=FixedSizeSplitter(chunk_size=20000, chunk_overlap=200),
)

# Run the pipeline on the PDF file
asyncio.run(kg_builder.run_async(file_path="reports/Report1.pdf"))

