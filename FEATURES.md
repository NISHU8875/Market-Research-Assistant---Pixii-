# Features Documentation

## 🎯 Overview

This document provides comprehensive documentation of all features in the Research Assistant RAG Agent, including the newly added Prompt Engineering and Web Search capabilities.

---

## 1. Prompt Engineering System

### 1.1 What is Prompt Engineering?

Prompt engineering in this context means tailoring the LLM's response style and output format based on the type of analysis or information extraction needed.

### 1.2 Available Prompt Templates

#### **General**
- **Use Case**: Default for all queries
- **Output Style**: Clear, conversational answers with key points
- **Best For**: General questions, summaries, explanations
- **Features**:
  - Organized responses
  - Cites sources
  - Uses basic formatting

#### **E-Commerce Analysis** ⭐ *NEW*
- **Use Case**: Amazon bestsellers, product data, market revenue analysis
- **Output Style**: Structured tables with metrics and insights
- **Best For**:
  - "What are the top 10 bestselling products?"
  - "Estimate monthly revenue for these products"
  - "Analyze market trends in this category"
- **Features**:
  - Tabular product rankings
  - Revenue calculations
  - Market insights
  - Competitive analysis
  - Formatted monetary values

#### **Market Research**
- **Use Case**: Competitive landscape, market size, trends
- **Output Style**: Analysis with comparison tables
- **Best For**:
  - Market size estimation
  - Competitor identification
  - Trend analysis
  - Opportunity assessment
- **Features**:
  - Competitive matrices
  - Trend identification
  - Market opportunity highlights
  - Clear sourcing

#### **Financial Analysis**
- **Use Case**: Financial metrics, ratios, performance data
- **Output Style**: Financial tables with calculations
- **Best For**:
  - Revenue analysis
  - Profit margin calculations
  - Growth rate comparisons
  - Financial risk assessment
- **Features**:
  - Financial tables
  - Ratio calculations
  - Trend analysis
  - Clear assumptions

#### **Data Extraction**
- **Use Case**: Structured data pulling from documents
- **Output Style**: Clean, organized data in tables
- **Best For**:
  - Contact information extraction
  - Product specifications
  - Price lists
  - Technical specifications
- **Features**:
  - Structured output
  - Data quality assessment
  - Missing data flagging
  - Source documentation

### 1.3 System Prompts

Each template has a **system prompt** that guides the LLM's overall behavior:

```python
# Example: E-Commerce Analysis System Prompt
"You are an E-commerce Intelligence Analyst. Your role is to:
1. Analyze product and market data from the provided sources
2. Extract key metrics like revenue, sales volume, and market trends
3. For Amazon bestseller data: Extract the top 10 products and estimate monthly revenue
4. Present findings in clear, tabular format when possible
5. Provide human-readable summaries with key insights
6. Always reference the data source
7. Highlight market opportunities and trends observed
8. Include competitor analysis if relevant"
```

### 1.4 Query Prompts

Each template also has a specific **query prompt** that formats the user's question and context:

```python
# Example: E-Commerce Query Prompt
"You are an E-commerce Intelligence Analyst analyzing market data.

Document Context:
{context}

User Query: {query}

Instructions:
- Extract relevant e-commerce metrics (revenue, sales, rankings, market trends)
- For top product queries, present data in a structured table format
- Include estimated metrics based on the provided data
- Clearly separate factual data from estimates
..."
```

### 1.5 How to Use Prompt Templates

1. **In UI**: Use the sidebar dropdown to select your template
2. **In Code**:
```python
from rag import generate

# Use specific template
answer, sources, search_info = generate(
    query="Your question here",
    prompt_template="ECOMMERCE_ANALYSIS"  # Choose template
)
```

### 1.6 Creating Custom Prompts (Advanced)

Edit `prompts_config.py` to add new templates:

```python
# Add to SYSTEM_PROMPTS
SYSTEM_PROMPTS["CUSTOM_TEMPLATE"] = """Your custom system prompt here..."""

# Add to QUERY_PROMPTS
QUERY_PROMPTS["CUSTOM_TEMPLATE"] = """Your custom query prompt here..."""

# Add to PromptTemplate enum
class PromptTemplate(Enum):
    CUSTOM = "CUSTOM"
```

---

## 2. Web Search Integration

### 2.1 What is Web Search Integration?

Web search allows the RAG agent to:
- Search the internet for supplementary information
- Combine document-based answers with current web data
- Prevent hallucination by grounding responses
- Clearly distinguish between document and web sources

### 2.2 How Web Search Works

```
User Query
    ↓
Retrieve from Documents
    ↓
Are documents sufficient? (confidence check)
    ↓ (if confidence < threshold)
Search the Web
    ↓
Combine Results (prioritize documents)
    ↓
Generate Grounded Response
    ↓
Add Source Attribution
```

### 2.3 Web Search Trigger Conditions

Web search is automatically triggered when:

1. **Query Requests Current Information**:
   - Keywords: "latest", "recent", "current", "today", "now", "2024", "2025", "2026"

2. **Query Requests Verification**:
   - Keywords: "verify", "confirm", "check", "validate", "is it true"

3. **Low Document Confidence** (< 30%):
   - When retrieved documents don't strongly match the query

### 2.4 Enabling Web Search

**In UI**:
- Toggle the **🌐 Enable Web Search** checkbox in the sidebar

**In Code**:
```python
from rag import generate

answer, sources, search_info = generate(
    query="What are the latest real estate trends?",
    use_web_search=True,  # Enable web search
    prompt_template="MARKET_RESEARCH"
)
```

### 2.5 Web Search Results Format

Web search results are presented with clear attribution:

```
**Solution**
Based on the provided documents...

**Web Search Results**
Additionally, web sources indicate...

**Sources**
📎 Document: https://example.com/article1
📎 Web Search: Recent market data
```

### 2.6 Preventing Hallucination

The system prevents hallucination by:

1. **Document Prioritization**: Answers primarily use documents
2. **Citation Tracking**: All information is attributed
3. **Source Separation**: Clear distinction between sources
4. **Confidence Checking**: Only supplements when needed
5. **Explicit Honesty**: States when information is unavailable

### 2.7 Web Search Requirements

To use web search:
- Install: `pip install duckduckgo-search>=3.9.10`
- Internet connection required
- No API key needed (DuckDuckGo is free)

If not installed, the UI shows: "⚠️ Web search not available"

---

## 3. Response Formatting

### 3.1 Output Formats

The LLM is instructed to output in these formats when appropriate:

#### **Tables** (Markdown format)

For E-Commerce Analysis:
```
| Rank | Product Name | Avg Rating | Est. Monthly Revenue |
|------|--------------|-----------|---------------------|
| 1    | Product A    | 4.8       | $2,500,000         |
| 2    | Product B    | 4.7       | $2,100,000         |
```

#### **Human-Readable Summary**

```
## Key Findings

**Top Performer**: Product A dominates with 4.8★ rating and estimated monthly revenue of $2.5M.

**Market Trends**: 
- Category showing 15% YoY growth
- Consumer preference shifting to eco-friendly products
- Price sensitivity decreasing in premium segment
```

#### **Structured Lists**

```
### Market Insights
- Opportunity 1: Market gap in X segment ($500M potential)
- Opportunity 2: Rising demand for Y feature
- Risk 1: Increasing competition from Z companies
```

### 3.2 Citation Format

All answers include citations:

```
[Source: https://example.com/product-data]
[Source: https://example.com/market-report]
[Web Search: Recent market trends]
```

---

## 4. Advanced Use Cases

### 4.1 E-Commerce Analysis Example

**Scenario**: Analyzing Amazon bestseller data

**Steps**:
1. Paste Amazon bestseller page URL
2. Click "🚀 Process URLs"
3. Select **E-Commerce Analysis** template
4. Ask: "What are the top 10 bestselling products and their estimated monthly revenue?"

**Expected Output**:
- Table with product rankings
- Revenue estimates
- Market share analysis
- Trend identification

### 4.2 Market Research Example

**Scenario**: Analyzing market competitive landscape

**Steps**:
1. Process competitor websites and market reports
2. Select **Market Research** template
3. Enable web search for latest developments
4. Ask: "Analyze the competitive landscape"

**Expected Output**:
- Competitor comparison matrix
- Market trends
- Strategic opportunities
- Risk assessment

### 4.3 Financial Analysis Example

**Scenario**: Analyzing financial reports

**Steps**:
1. Process financial documents/reports
2. Select **Financial Analysis** template
3. Ask: "What are the key financial metrics and trends?"

**Expected Output**:
- Financial metrics table
- Ratio analysis
- Growth trends
- Risk indicators

---

## 5. Configuration & Customization

### 5.1 Adjusting LLM Parameters

Edit `rag.py`:

```python
# Adjust temperature (0.0 = deterministic, 1.0 = creative)
llm = ChatGroq(
    model='llama-3.3-70b-versatile',
    temperature=0.5,  # Lower for more consistent results
    max_tokens=1000   # Increase for longer responses
)
```

### 5.2 Changing Chunk Size

Edit `rag.py`:

```python
CHUNK_SIZE = 1500  # Larger chunks = more context
CHUNK_OVERLAP = 300  # Overlap for continuity
```

### 5.3 Different Embedding Models

Edit `rag.py`:

```python
EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'  # Faster, less accurate
EMBEDDING_MODEL = 'Alibaba-NLP/gte-large-en-v1.5'  # Larger, more accurate
```

### 5.4 Web Search Trigger Tuning

Edit `search_tools.py`:

```python
def should_search_web(self, query: str, document_confidence: float = 0.5):
    # Adjust confidence threshold
    # Adjust keywords list
    # Add custom logic
```

---

## 6. Performance Optimization

### 6.1 Speed Improvements

- **Reduce Chunk Size**: Faster retrieval, less context
- **Fewer Chunks Returned**: Change `k=2` to `k=1` in rag.py
- **Disable Web Search**: When not needed
- **Use Faster Embeddings**: MiniLM instead of gte-base

### 6.2 Quality Improvements

- **Increase Chunk Size**: More context per chunk
- **Increase Chunks Returned**: More options to choose from
- **Enable Web Search**: For current information
- **Choose Right Template**: Aligned with task
- **Use Better Embeddings**: gte-large for accuracy

### 6.3 Memory Optimization

- **Process URLs in Batches**: Avoid loading all at once
- **Regular Vector Store Cleanup**: Remove old documents
- **Separate Collections**: Different domains in separate stores

---

## 7. Troubleshooting Advanced Features

### Issue: "Templates not changing effect"
**Solution**: Verify template name matches exactly (case-sensitive)

### Issue: "Web search results not appearing"
**Solution**: 
1. Check: `pip list | grep duckduckgo`
2. Ensure internet connection
3. Check DuckDuckGo rate limits (if many searches)

### Issue: "Responses not using template style"
**Solution**:
1. Check `current_prompt_template` is set correctly
2. Verify LLM received the system prompt
3. Check temperature isn't too high

### Issue: "Hallucination still occurring"
**Solution**:
1. Enable web search for verification
2. Use more specific queries
3. Process more relevant documents
4. Reduce temperature in LLM settings

---

## 8. Future Enhancements

Planned features:
- [ ] Custom prompt template creation UI
- [ ] Multi-language support
- [ ] Real-time web search integration
- [ ] PDF/document upload
- [ ] Chain-of-thought reasoning templates
- [ ] Multi-step analysis templates
- [ ] RAG pipeline visualization
- [ ] A/B testing for prompts
- [ ] Response quality scoring
- [ ] Feedback loop for prompt optimization

---

## 9. API Reference

### Core Functions

#### `generate(query, use_web_search=False, prompt_template="GENERAL")`

Generates response to a query.

**Parameters**:
- `query` (str): User question
- `use_web_search` (bool): Enable web search (default: False)
- `prompt_template` (str): Template name (default: "GENERAL")

**Returns**: Tuple of (answer, sources, search_info)

#### `set_prompt_template(template_name)`

Sets the active prompt template.

**Parameters**:
- `template_name` (str): Template to activate

**Returns**: bool (success/failure)

#### `get_available_prompt_templates()`

Gets list of available templates.

**Returns**: List of template names

#### `is_web_search_available()`

Checks if web search is available.

**Returns**: bool (available/unavailable)

---

**Version**: 2.0.0  
**Last Updated**: May 2026  
**Status**: Stable with Active Development
