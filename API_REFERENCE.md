# API Reference

Complete API documentation for integrating and extending the Research Assistant RAG Agent.

---

## Table of Contents

1. [RAG Module](#rag-module)
2. [Prompts Configuration](#prompts-configuration)
3. [Search Tools](#search-tools)
4. [Data Types](#data-types)
5. [Examples](#examples)

---

## RAG Module

Core RAG engine for document processing and query handling.

### `rag.py`

#### Functions

##### `initialize()`

Initializes global components (LLM, vector store, search manager).

```python
from rag import initialize

initialize()  # Must be called before other functions
```

**Parameters**: None  
**Returns**: None  
**Raises**: API errors if Groq key invalid

---

##### `reset_vector_store()`

Clears all stored vectors and documents from ChromaDB.

```python
from rag import reset_vector_store

reset_vector_store()  # Wipe all data
```

**Parameters**: None  
**Returns**: None  
**Side Effects**: Deletes all documents from vector store

---

##### `process_urls(urls: List[str])`

Processes URLs, extracts content, chunks, and stores in vector database.

```python
from rag import process_urls

urls = [
    "https://example.com/article1",
    "https://example.com/article2"
]

for status in process_urls(urls):
    print(status)
    # Output:
    # "Loading data from url"
    # "Data loaded, Creating chunks"
    # "Chunks created, storing in a vector store.."
```

**Parameters**:
- `urls` (List[str]): URLs to process (1-3 recommended)

**Yields**: Status messages (str)

**Process Flow**:
1. Load URL content using WebBaseLoader
2. Split into chunks (1000 chars, 200 overlap)
3. Generate embeddings using HuggingFace
4. Store vectors in ChromaDB

**Exceptions**:
- `HTTPError`: Invalid or unreachable URL
- `ValueError`: Content extraction failed

---

##### `generate(query: str, use_web_search: bool = False, prompt_template: str = "GENERAL") -> Tuple[str, List[str], Optional[str]]`

Generates response to user query with optional web search.

```python
from rag import generate

# Basic usage
answer, sources, search_info = generate("What is the main topic?")

# With web search
answer, sources, search_info = generate(
    query="What are the latest trends?",
    use_web_search=True
)

# With specific template
answer, sources, search_info = generate(
    query="Top 10 products by revenue?",
    prompt_template="ECOMMERCE_ANALYSIS"
)
```

**Parameters**:
- `query` (str): User question
- `use_web_search` (bool): Enable web search (default: False)
- `prompt_template` (str): Prompt template name (default: "GENERAL")

**Returns**: Tuple of:
- `answer` (str): LLM response
- `sources` (List[str]): Document source URLs
- `search_info` (Optional[str]): Search usage note

**Raises**:
- `RuntimeError`: Vector store not initialized
- `RuntimeError`: No documents found

---

##### `set_prompt_template(template_name: str) -> bool`

Sets the active prompt template for subsequent queries.

```python
from rag import set_prompt_template

# Set template
success = set_prompt_template("ECOMMERCE_ANALYSIS")

if success:
    print("Template set successfully")
else:
    print("Invalid template name")
```

**Parameters**:
- `template_name` (str): Name of template to activate

**Returns**: bool (True if valid template, False otherwise)

**Valid Templates**:
- "GENERAL"
- "ECOMMERCE_ANALYSIS"
- "MARKET_RESEARCH"
- "FINANCIAL_ANALYSIS"
- "DATA_EXTRACTION"

---

##### `get_available_prompt_templates() -> List[str]`

Returns list of all available prompt templates.

```python
from rag import get_available_prompt_templates

templates = get_available_prompt_templates()
print(templates)
# Output: ['GENERAL', 'ECOMMERCE_ANALYSIS', 'MARKET_RESEARCH', ...]
```

**Parameters**: None  
**Returns**: List[str] of template names

---

##### `get_prompt_template_descriptions() -> Dict[str, str]`

Returns descriptions for all templates.

```python
from rag import get_prompt_template_descriptions

descs = get_prompt_template_descriptions()
for name, desc in descs.items():
    print(f"{name}: {desc}")
```

**Returns**: Dict mapping template names to descriptions

---

##### `is_web_search_available() -> bool`

Checks if web search functionality is available.

```python
from rag import is_web_search_available

if is_web_search_available():
    print("Web search enabled")
else:
    print("Web search not available - install duckduckgo-search")
```

**Returns**: bool (True if DuckDuckGo installed, False otherwise)

---

## Prompts Configuration

Prompt templates and system instructions for LLM behavior.

### `prompts_config.py`

#### Classes

##### `PromptTemplate(Enum)`

Enumeration of available prompt templates.

```python
from prompts_config import PromptTemplate

# Access template names
template = PromptTemplate.ECOMMERCE_ANALYSIS
print(template.value)  # Output: "ECOMMERCE_ANALYSIS"

# Iterate all templates
for template in PromptTemplate:
    print(template.value)
```

**Members**:
- `GENERAL`: General purpose Q&A
- `ECOMMERCE_ANALYSIS`: E-commerce data analysis
- `MARKET_RESEARCH`: Market analysis
- `FINANCIAL_ANALYSIS`: Financial data analysis
- `DATA_EXTRACTION`: Structured data extraction

---

#### Functions

##### `get_system_prompt(template_type: str = "GENERAL") -> str`

Gets system prompt for specified template.

```python
from prompts_config import get_system_prompt

prompt = get_system_prompt("ECOMMERCE_ANALYSIS")
print(prompt)
# Output: "You are an E-commerce Intelligence Analyst..."
```

**Parameters**:
- `template_type` (str): Template name

**Returns**: str (system prompt)

---

##### `get_query_prompt(template_type: str = "GENERAL") -> str`

Gets query prompt template for specified template.

```python
from prompts_config import get_query_prompt

prompt = get_query_prompt("MARKET_RESEARCH")
# This prompt includes {context} and {query} placeholders
```

**Parameters**:
- `template_type` (str): Template name

**Returns**: str (prompt template with {context} and {query} placeholders)

---

##### `list_available_templates() -> List[str]`

Lists all available templates.

```python
from prompts_config import list_available_templates

templates = list_available_templates()
# Output: ['GENERAL', 'ECOMMERCE_ANALYSIS', ...]
```

**Returns**: List[str] of template names

---

##### `get_template_description() -> Dict[str, str]`

Gets descriptions for all templates.

```python
from prompts_config import get_template_description

descriptions = get_template_description()
for name, desc in descriptions.items():
    print(f"{name}: {desc}")
```

**Returns**: Dict[str, str] (template name → description)

---

## Search Tools

Web search integration and response grounding.

### `search_tools.py`

#### Classes

##### `WebSearchManager`

Manages web search queries and results.

```python
from search_tools import WebSearchManager

manager = WebSearchManager()

# Check availability
if manager.is_search_available():
    results = manager.search("machine learning trends")
    print(results)
```

**Methods**:

###### `__init__()`

Initializes search manager.

```python
manager = WebSearchManager()
```

---

###### `search(query: str, max_results: int = 3) -> Optional[str]`

Performs web search.

```python
results = manager.search("real estate market trends", max_results=5)

if results:
    print(results)
else:
    print("Search not available or failed")
```

**Parameters**:
- `query` (str): Search query
- `max_results` (int): Maximum results (default: 3)

**Returns**: Optional[str] (search results or None)

**Raises**: None (catches internally)

---

###### `is_search_available() -> bool`

Checks if search is available.

```python
if manager.is_search_available():
    print("DuckDuckGo available")
else:
    print("Install duckduckgo-search")
```

**Returns**: bool

---

###### `format_search_results(results: str) -> str`

Formats search results for display.

```python
formatted = manager.format_search_results(raw_results)
print(formatted)
# Output: "**Web Search Results:**\n..."
```

**Parameters**:
- `results` (str): Raw search results

**Returns**: str (formatted for markdown display)

---

##### `GroundedResponseGenerator`

Ensures responses are grounded in document context.

```python
from search_tools import GroundedResponseGenerator

generator = GroundedResponseGenerator(retrieved_docs)
```

**Methods**:

###### `__init__(vector_store_results: List[Dict])`

Initializes with retrieved documents.

```python
# From vector store retrieval
results = vector_store.similarity_search(query, k=2)
generator = GroundedResponseGenerator(results)
```

**Parameters**:
- `vector_store_results`: Retrieved document chunks

---

###### `should_search_web(query: str, document_confidence: float = 0.5) -> bool`

Determines if web search should be performed.

```python
if generator.should_search_web(query, confidence=0.6):
    # Perform web search
    pass
```

**Parameters**:
- `query` (str): User query
- `document_confidence` (float): Confidence in documents (0-1)

**Returns**: bool

**Triggers Web Search**:
- Current information keywords: "latest", "recent", "2024", "2025"
- Verification keywords: "verify", "confirm", "check"
- Low document confidence (< 0.3)

---

###### `generate_grounded_response_prompt(query: str, context: str, web_results: Optional[str] = None, use_search: bool = False) -> str`

Generates prompt ensuring grounded response.

```python
prompt = generator.generate_grounded_response_prompt(
    query="Market trends?",
    context="Retrieved document content",
    web_results="Search results if any",
    use_search=True
)

# Use prompt with LLM
response = llm.invoke(prompt)
```

**Parameters**:
- `query` (str): User question
- `context` (str): Document context
- `web_results` (Optional[str]): Web search results
- `use_search` (bool): Whether search was used

**Returns**: str (formatted prompt)

---

#### Functions

##### `create_grounded_analysis(query: str, context: str, web_results: Optional[str] = None, include_search_note: bool = False) -> Tuple[str, List[str]]`

Creates analysis prompt and citation guidelines.

```python
from search_tools import create_grounded_analysis

prompt, citations = create_grounded_analysis(
    query="Analyze this data",
    context="Document context",
    web_results="Web search results",
    include_search_note=True
)
```

**Parameters**:
- `query` (str): User query
- `context` (str): Document context
- `web_results` (Optional[str]): Search results
- `include_search_note` (bool): Include search note (default: False)

**Returns**: Tuple of:
- `prompt` (str): Analysis prompt
- `citation_guidelines` (List[str]): How to cite sources

---

## Data Types

### Response Tuple

All `generate()` calls return:

```python
answer: str  # LLM response
sources: List[str]  # Document URLs
search_info: Optional[str]  # Search usage note (e.g., "Web search results included")
```

### Document Metadata

Documents stored in ChromaDB have metadata:

```python
{
    "source": "https://example.com/article",
    "page_content": "Document text content...",
    "metadata": {
        # Additional metadata from WebBaseLoader
    }
}
```

### Configuration

```python
# rag.py constants
CHUNK_SIZE = 1000  # Characters per chunk
CHUNK_OVERLAP = 200  # Overlap between chunks
COLLECTION_NAME = "real_estate"
EMBEDDING_MODEL = "Alibaba-NLP/gte-base-en-v1.5"

# LLM Settings
LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 700
```

---

## Examples

### Example 1: Basic Query

```python
from rag import initialize, process_urls, generate

# Setup
initialize()

# Process URL
urls = ["https://example.com/article"]
for status in process_urls(urls):
    print(status)

# Query
answer, sources, search_info = generate("What is the main topic?")
print(f"Answer: {answer}")
print(f"Sources: {sources}")
```

### Example 2: E-Commerce Analysis

```python
from rag import generate, set_prompt_template

# Set template
set_prompt_template("ECOMMERCE_ANALYSIS")

# Query with web search
answer, sources, search_info = generate(
    query="What are the top 10 bestselling products and their estimated revenue?",
    use_web_search=True
)

print(answer)  # Tabular format with products and revenue
```

### Example 3: Custom Prompt Template

```python
from prompts_config import get_system_prompt, get_query_prompt

# Get templates
system = get_system_prompt("FINANCIAL_ANALYSIS")
query_template = get_query_prompt("FINANCIAL_ANALYSIS")

# Use with LLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", query_template)
])

llm = ChatGroq(model="llama-3.3-70b-versatile")
chain = chat_prompt | llm

result = chain.invoke({
    "context": "Financial data here",
    "query": "What are the key metrics?"
})
```

### Example 4: Web Search Integration

```python
from search_tools import WebSearchManager, GroundedResponseGenerator

# Initialize
manager = WebSearchManager()
generator = GroundedResponseGenerator([])

# Check availability
if manager.is_search_available():
    # Perform search
    results = manager.search("artificial intelligence trends")
    
    # Generate grounded prompt
    prompt = generator.generate_grounded_response_prompt(
        query="What are AI trends?",
        context="Document content",
        web_results=results,
        use_search=True
    )
```

### Example 5: Complete Integration

```python
from rag import initialize, process_urls, generate, get_available_prompt_templates
from streamlit import sidebar, chat_message, chat_input

# Initialize
initialize()

# UI
templates = get_available_prompt_templates()
selected = sidebar.selectbox("Choose template", templates)

urls = sidebar.text_input("URLs").split(",")
if sidebar.button("Process"):
    for status in process_urls(urls):
        st.write(status)

query = chat_input("Ask question")
if query:
    answer, sources, search_info = generate(
        query=query,
        prompt_template=selected,
        use_web_search=sidebar.checkbox("Enable web search")
    )
    
    with chat_message("assistant"):
        st.write(answer)
        if search_info:
            st.info(search_info)
        for source in sources:
            st.markdown(f"📎 {source}")
```

---

## Constants & Enums

### Template Names

```python
"GENERAL"
"ECOMMERCE_ANALYSIS"
"MARKET_RESEARCH"
"FINANCIAL_ANALYSIS"
"DATA_EXTRACTION"
```

### Environment Variables

```
GROQ_API_KEY  # Required: Groq API key
CHUNK_SIZE  # Optional: Characters per chunk (default: 1000)
```

### Error Messages

```
"Vector store not initialized"
"No documents found"
"You must process the url first"
"Invalid template name"
```

---

## Performance Tips

1. **Reduce Latency**:
   - Use `k=1` in similarity_search
   - Reduce CHUNK_SIZE
   - Disable web search

2. **Improve Quality**:
   - Increase `k` (more chunks)
   - Use larger embedding model
   - Enable web search for current info

3. **Optimize Memory**:
   - Process URLs in batches
   - Clear vector store periodically
   - Use smaller embedding models

---

## Extension Points

Extend the system by:

1. **Custom Prompt Templates**: Add to `prompts_config.py`
2. **New Search Tools**: Extend `search_tools.py`
3. **LLM Providers**: Add to `rag.py` initialization
4. **UI Components**: Extend `main.py` Streamlit interface

---

**Version**: 2.0.0  
**Last Updated**: May 2026  
**Maintained By**: NISHU KUMAR
