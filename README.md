# Medical Dataset Knowledge Graph Builder

This project creates knowledge graphs from medical PDF reports using Neo4j GraphRAG and OpenAI. It provides multiple approaches for building knowledge graphs with different levels of schema control.

## Prerequisites

Before getting started, ensure you have the following installed and configured:

### 1. Install uv
Install `uv` (Python package manager):

### 2. Clone the Repository
```bash
git clone https://github.com/neo4j-product-examples/graphrag-package-1.8-examples.git
cd graphrag-package-1.8-examples
```

### 3. Create Virtual Environment with uv
```bash
uv venv
source .venv/bin/activate
```

### 4. Install Dependencies with uv sync
```bash
uv sync
```

### 5. Set Up Environment Variables
Create a `.env` file in the root directory with the following variables:

```env
# OpenAI Configuration (Required)
OPENAI_API_KEY=your_openai_api_key_here

# Neo4j Database Configuration
NEO4J_URI=neo4j+s://<your_aura_instance_id>.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password_here
NEO4J_DATABASE=neo4j
```

**Important Notes:**
- `OPENAI_API_KEY` is **required** for all operations
- Neo4j variables have defaults but should be configured for your specific setup
- Make sure your Neo4j database is running and accessible

## Usage

The project provides four different approaches to create knowledge graphs from medical reports:

### 1. Create KG with No Schema Provided

This approach uses automatic schema extraction without providing a predefined schema.

```bash
python create-kg-no-schema.py
```

**What it does:**
- Automatically extracts schema from the medical report content
- Creates a knowledge graph without predefined structure
- Uses `Report1.pdf` as the input document

### 2. Create KG with Schema

This approach uses a predefined schema to structure the knowledge graph.

```bash
python create-kg-with-schema.py
```

**What it does:**
- Uses a predefined schema with specific node types and relationships
- Includes entities like Patient, Physician, Medical Institution, Symptoms, etc.
- Provides more structured and consistent knowledge graph output

### 3. Create KG with Improved Schema

This approach uses an enhanced version of the schema for better knowledge graph quality.

```bash
python create-kg-with-improved-schema.py
```

**What it does:**
- Uses an improved schema with better-defined relationships and properties
- Information from Symptom is moved to the relationship type!

### 4. Use LLM to Generate & Save Schema

This approach generates a schema using LLM analysis and saves it for future use.

```bash
python extract-save-schema.py
```

**What it does:**
- Analyzes medical reports to automatically generate an appropriate schema
- Saves the generated schema to `medical-report-schema.json`
- Can be used as input for other knowledge graph creation methods

## Project Structure

```
medical-dataset/
├── create-kg-no-schema.py          # No schema approach
├── create-kg-with-schema.py        # Predefined schema approach
├── create-kg-with-improved-schema.py  # Enhanced schema approach
├── extract-save-schema.py          # Schema generation and saving
├── medical-report-schema.json      # Generated/saved schema file
├── reports/                        # Medical PDF reports directory
│   ├── Report1.pdf
│   ├── report2.pdf
│   └── ...
├── pyproject.toml                  # Project configuration
├── .env                           # Environment variables (create this)
└── README.md                      # This file
```

## Dependencies

The project uses the following main dependencies:
- `neo4j-graphrag>=1.8.0` - Neo4j GraphRAG library
- `neo4j-rust-ext>=5.28.1.0` - Neo4j extensions
- `openai>=1.97.0` - OpenAI API client
- `python-dotenv>=1.1.1` - Environment variable management

## Requirements

- Python >= 3.13
- OpenAI API access (API key required)
- Neo4j database (local or remote)
- PDF medical reports in the `reports/` directory

## Troubleshooting

### Common Issues

1. **Missing OpenAI API Key**: Ensure `OPENAI_API_KEY` is set in your `.env` file
2. **Neo4j Connection Error**: Verify your Neo4j database is running and connection details are correct
3. **PDF Not Found**: Make sure PDF files are in the `reports/` directory

### Support

For issues with:
- Neo4j GraphRAG: Check the [official documentation](https://neo4j.com/docs/graph-data-science/)
- OpenAI API: Visit [OpenAI API documentation](https://platform.openai.com/docs/)
- uv package manager: See [uv documentation](https://docs.astral.sh/uv/)
