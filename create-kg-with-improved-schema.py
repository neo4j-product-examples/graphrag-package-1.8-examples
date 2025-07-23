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

NODE_TYPES = [
    # Node types can be defined with a simple label
    {"label": "Patient", "properties": [
        {"name": "name", "type": "STRING", "required": True}, 
        {"name": "age", "type": "INTEGER"}, 
        {"name": "gender", "type": "STRING"}, 
        {"name": "DOB", "type": "STRING"}]},
    {"label": "Medical Institution", "properties": [
        {"name": "name", "type": "STRING", "required": True}, 
        {"name": "address", "type": "STRING"}]},
    {"label": "Physician", "properties": [
        {"name": "name", "type": "STRING", "required": True}, 
        {"name": "specialty", "type": "STRING"}]},
    {"label": "Symptom", "properties": [
        {"name": "name", "type": "STRING", "required": True}]},
    {"label": "Medication", "properties": [
        {"name": "name", "type": "STRING", "required": True}, {"name": "dosage", "type": "STRING"}]},
    {"label": "Condition", "description": "A medical condition or disease", "properties": [
        {"name": "name", "type": "STRING", "required": True}, {"name": "description", "type": "STRING"}]},
    {"label": "Imaging", "properties": [
        {"name": "name", "type": "STRING", "required": True}, {"name": "description", "type": "STRING"}]},
    {"label": "Lab Test", "properties": [
        {"name": "name", "type": "STRING", "required": True}, 
        {"name": "description", "type": "STRING"}, 
        {"name": "result", "type": "STRING"}]},    
]

# Same for relationships:
RELATIONSHIP_TYPES = [
    "REFERRED_BY",
    {
        "label": "HAS_SYMPTOM",
        "properties": [
            {"name": "patient_description", "type": "STRING"}, 
            {"name": "severity", "type": "STRING"}, 
            {"name": "duration", "type": "STRING"}, 
            {"name": "clinical_notes", "type": "STRING"}
        ]
    },
    "HAS_CONDITION",
    "HAD_IMAGING",
    "HAD_LAB_TEST",
    "PRESCRIBED_MEDICATION",
    "PRIMARY_MEDICAL_INSTITUTION",
    "WAS_SEEN_AT"
]

PATTERNS = [
    ("Patient", "REFERRED_BY", "Physician"),
    ("Patient", "HAS_SYMPTOM", "Symptom"),
    ("Patient", "HAS_CONDITION", "Condition"),
    ("Patient", "HAD_IMAGING", "Imaging"),
    ("Patient", "HAD_LAB_TEST", "Lab Test"),
    ("Patient", "PRESCRIBED_MEDICATION", "Medication"),
    ("Physician", "PRIMARY_MEDICAL_INSTITUTION", "Medical Institution"),
    ("Patient", "WAS_SEEN_AT", "Medical Institution"),
]

kg_builder = SimpleKGPipeline(
    llm=llm,
    driver=driver,
    embedder=embedder,
    schema ={
      "node_types": NODE_TYPES,
      "relationship_types": RELATIONSHIP_TYPES,
      "patterns": PATTERNS,
      "additional_node_types": True,
      "additional_relationship_types": True,
      "additional_patterns": True,
    },
    from_pdf=True,
    text_splitter=FixedSizeSplitter(chunk_size=20000, chunk_overlap=200),
)


# Run the pipeline on the PDF file
asyncio.run(kg_builder.run_async(file_path="reports/report3.pdf"))

