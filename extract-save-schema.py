import asyncio
import neo4j
import os
from dotenv import load_dotenv
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from neo4j_graphrag.experimental.components.text_splitters.fixed_size_splitter import FixedSizeSplitter
from neo4j_graphrag.experimental.components.pdf_loader import PdfLoader
from neo4j_graphrag.experimental.components.schema import SchemaFromTextExtractor, GraphSchema
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from fsspec.implementations.local import LocalFileSystem

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

async def main():
    # Create a local filesystem instance
    fs = LocalFileSystem()
    
    # Extract schema using LLM and save to JSON file or YAML file
    schema_extractor = SchemaFromTextExtractor(llm=llm)
    inferred_schema = await schema_extractor.run(text=PdfLoader.load_file("reports/report5.pdf", fs=fs))
    inferred_schema.save("medical-report-schema.json")

    # Create a SimpleKGPipeline instance loading schema previously created. 
    extracted_schema = GraphSchema.from_file("medical-report-schema.json")
    kg_builder = SimpleKGPipeline(
        llm=llm,
        driver=driver,
        embedder=embedder,
        from_pdf=True,
        text_splitter=FixedSizeSplitter(chunk_size=20000, chunk_overlap=200),
        schema=extracted_schema,
    )

    # Run the pipeline on the PDF file
    await kg_builder.run_async(file_path="reports/report5.pdf")

if __name__ == "__main__":
    asyncio.run(main())

