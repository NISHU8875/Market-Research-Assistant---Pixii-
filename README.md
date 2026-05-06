# 🔍 Market Research Assistant -  Pixii :")

A powerful **Retrieval-Augmented Generation (RAG)** agent that extracts and analyzes relevant information from URLs. Drop a URL, process it into a vector database, and query it using AI-powered conversational capabilities with prompt engineering and optional web search.

---

## ✨ Key Features

### 📥 **Smart URL Processing**
- Process multiple URLs simultaneously
- Automatic content extraction using WebBaseLoader
- Intelligent chunking with RecursiveCharacterTextSplitter
- Vector embedding storage in ChromaDB for fast retrieval

### 📝 **Advanced Prompt Engineering**
Choose from multiple response styles tailored to your use case:
- **General**: Standard Q&A and analysis
- **E-Commerce Analysis**: Extract revenue metrics, bestseller rankings, market insights (perfect for Amazon data)
- **Market Research**: Competitive analysis and trend identification
- **Financial Analysis**: Financial metrics extraction and interpretation
- **Data Extraction**: Structured data extraction in tabular format

### 🌐 **Web Search Integration** (Optional)
- Augment document-based answers with web search
- Grounded responses prioritizing document information
- Clear distinction between document sources and external knowledge
- Prevents hallucination with source attribution

### 💬 **Conversational AI**
- Multi-turn conversation with history tracking
- LLM-powered responses using Groq's Llama 3.3
- Source attribution with clickable links
- Human-readable and tabular output formatting

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Streamlit Frontend UI                      │
│        (Chat Interface + Configuration Panel)                │
└────────────┬────────────────────────────────┬────────────────┘
             │                                │
             ▼                                ▼
    ┌─────────────────┐        ┌──────────────────────────┐
    │  URL Processing │        │  Prompt Engineering      │
    │   Module (RAG)  │        │  Config (prompts_config) │
    └────────┬────────┘        └──────────────────────────┘
             │                                │
             ▼                                ▼
    ┌─────────────────┐        ┌──────────────────────────┐
    │  WebBaseLoader  │        │  LLM (Groq - Llama 3.3)  │
    │  + BS4          │        │  with System Prompts     │
    └────────┬────────┘        └──────────────────────────┘
             │                                │
             ▼                                │
    ┌─────────────────────────┐              │
    │  RecursiveCharacter     │◄─────────────┘
    │  TextSplitter           │              ┌─────────────────┐
    │  (CHUNK_SIZE: 1000)     │────────────►│ Web Search Tool │
    └────────┬────────────────┘             │  (DuckDuckGo)   │
             │                              └─────────────────┘
             ▼
    ┌─────────────────────────┐
    │  HuggingFace Embeddings │
    │  (gte-base-en-v1.5)     │
    └────────┬────────────────┘
             │
             ▼
    ┌─────────────────────────┐
    │  ChromaDB Vector Store  │
    │  (./resources/vectorstore)
    └─────────────────────────┘
```

### **Data Flow**

1. **URL Input** → User pastes URLs in the sidebar
2. **Processing** → URLs are fetched and content is extracted
3. **Chunking** → Text is split into chunks for embedding
4. **Embedding** → Chunks converted to vectors using HuggingFace
5. **Storage** → Vectors stored in ChromaDB for retrieval
6. **Query** → User asks questions in chat
7. **Retrieval** → Most relevant chunks retrieved from vector store
8. **LLM Processing** → Prompt template applied with system instructions
9. **Web Search** (Optional) → Additional information from web if enabled
10. **Response** → Human-readable answer with source attribution

---

## 📁 Project Structure

```
research-assistant-rag-agent/
│
├── main.py                    # Streamlit UI application
├── rag.py                     # Core RAG logic and LLM integration
├── prompts_config.py          # Prompt templates and system prompts
├── search_tools.py            # Web search integration (DuckDuckGo)
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (GROQ_API_KEY)
├── README.md                  # This file
│
├── resources/
│   └── vectorstore/           # ChromaDB persistent storage
│       └── chroma-*.db        # Vector database files
│
└── assets/
    ├── architecture.png       # Architecture diagram
    ├── sc1.png               # Screenshot 1
    └── sc2.png               # Screenshot 2
```

### **File Descriptions**

#### `main.py` - User Interface
- Streamlit application entry point
- Chat interface and message history
- Sidebar for URL input and configuration
- Prompt template selector
- Web search toggle

#### `rag.py` - RAG Engine
- Vector store initialization and management
- URL processing and document chunking
- LLM interaction with prompt templates
- Web search integration
- Response generation with source attribution

#### `prompts_config.py` - Prompt Engineering
- Predefined prompt templates for different use cases
- System prompts for LLM behavior guidance
- Query-specific prompt formatting
- Template descriptions and helpers

#### `search_tools.py` - Web Search Module
- WebSearchManager: Manages web search queries
- GroundedResponseGenerator: Ensures responses are grounded in documents
- Citation and source tracking
- Prevents hallucination by prioritizing document information

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API Key (free at [console.groq.com](https://console.groq.com))

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/NISHU8875/Market-Research-Assistant---Pixii-.git
cd research-assistant-rag-agent
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Environment**
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key from: https://console.groq.com/keys

4. **Run the Application**
```bash
streamlit run main.py
```

The app will open at `http://localhost:8501`

---

## 📖 Usage Guide

### Step 1: Process URLs
1. Enter one or more URLs in the sidebar
2. Click **🚀 Process URLs** button
3. Wait for the status: "✅ Chunks stored! You can now ask questions"

### Step 2: Configure Response Style
- Use the **📝 Prompt Template** dropdown to select response style
- Choose based on your use case (General, E-Commerce, Market Research, etc.)

### Step 3: Optional Web Search
- Toggle **🌐 Enable Web Search** for supplementary information
- Useful for current information or verification

### Step 4: Ask Questions
- Type your question in the **💬 Chat** box
- Get AI-powered answers with source attribution
- View conversation history above

---

## 💡 Example Use Cases

### E-Commerce Analysis
**Question**: "What are the top 10 bestselling products on Amazon and their estimated monthly revenue?"

**Response Style**: E-Commerce Analysis

**Output**: Tabular breakdown with product names, rankings, and revenue estimates

### Market Research
**Question**: "Analyze the competitive landscape in the real estate market"

**Response Style**: Market Research

**Output**: Competitor comparison, market trends, and opportunities

### Financial Analysis
**Question**: "What are the key financial metrics mentioned in the documents?"

**Response Style**: Financial Analysis

**Output**: Tables with financial data, ratios, and trend analysis

### General Query
**Question**: "Summarize the main points from the documents"

**Response Style**: General

**Output**: Clear, concise summary with key insights

---

## 🔧 Configuration

### Model Parameters (in `rag.py`)

```python
CHUNK_SIZE = 1000              # Characters per chunk
COLLECTION_NAME = "real_estate"  # Vector store collection
EMBEDDING_MODEL = 'Alibaba-NLP/gte-base-en-v1.5'  # Embedding model
```

### LLM Parameters

- **Model**: Llama 3.3 (via Groq)
- **Temperature**: 0.7 (creativity level)
- **Max Tokens**: 700 (response length)

Modify in `rag.py`:
```python
llm = ChatGroq(
    model='llama-3.3-70b-versatile',
    temperature=0.7,
    max_tokens=700
)
```

### Embedding Model

The project uses HuggingFace embeddings for semantic understanding:
- Model: `Alibaba-NLP/gte-base-en-v1.5`
- Automatically downloaded on first use
- Provides high-quality semantic embeddings

---

## 📚 Technology Stack

### Core Libraries
| Technology | Purpose | Version |
|-----------|---------|---------|
| LangChain | RAG framework | 0.4.1+ |
| Streamlit | UI framework | 1.46.0+ |
| Chroma | Vector database | 1.0.0 |
| Groq | LLM provider | API-based |
| HuggingFace | Embeddings | 1.1.0 |

### Dependencies
- **langchain-community**: Document loaders, tools
- **langchain-chroma**: Vector store integration
- **langchain-groq**: LLM integration
- **sentence-transformers**: Embedding models
- **beautifulsoup4**: HTML parsing for web scraping
- **duckduckgo-search**: Web search capability
- **python-dotenv**: Environment configuration

---

## 🔐 Privacy & Security

- **Local Storage**: All documents and embeddings stored locally in `./resources/vectorstore/`
- **No Cloud Upload**: Document content never uploaded to external servers
- **API Keys**: Stored in local `.env` file (not version controlled)
- **Source Attribution**: Always knows where information comes from

### Add to `.gitignore`:
```
.env
resources/vectorstore/*
__pycache__/
*.pyc
.streamlit/secrets.toml
```

---

## 🐛 Troubleshooting

### Issue: "Vector store not initialized"
**Solution**: Click **🚀 Process URLs** before asking questions

### Issue: "No documents found"
**Solution**: Ensure URLs were processed successfully and contain valid content

### Issue: Web search not available
**Solution**: Install duckduckgo-search: `pip install duckduckgo-search>=3.9.10`

### Issue: Slow response
**Cause**: Large documents or many chunks being processed
**Solution**: 
- Reduce CHUNK_SIZE in rag.py
- Process fewer URLs at once
- Use web search sparingly

### Issue: Embedding model download fails
**Solution**: Manually download using:
```python
from langchain_huggingface import HuggingFaceEmbeddings
ef = HuggingFaceEmbeddings(model_name='Alibaba-NLP/gte-base-en-v1.5')
```

---

## 📈 Performance Optimization

### Tips for Better Results

1. **Quality URLs**: Process high-quality, content-rich URLs
2. **Specific Queries**: Ask specific questions for precise answers
3. **Template Selection**: Choose the right prompt template for your use case
4. **Chunk Overlap**: Maintain 200-character overlap for context continuity
5. **Web Search**: Use for current information, not for historical data

### Scaling Considerations

- **Multiple Collections**: Create separate collections for different domains
- **Batch Processing**: Process URLs in smaller batches
- **Cache Results**: ChromaDB automatically caches embeddings
- **Async Loading**: Modify WebBaseLoader for parallel URL loading

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contributions
- Additional prompt templates
- Support for more LLM providers
- PDF/document upload support
- Multi-language support
- Advanced web search filters
- Performance optimizations

---

## 📋 Roadmap

- [ ] PDF and document upload support
- [ ] Multi-language query support
- [ ] Advanced filtering and search operators
- [ ] User authentication and session management
- [ ] Export results to CSV/JSON
- [ ] Batch processing with job queue
- [ ] Custom prompt template creation UI
- [ ] Integration with more LLM providers
- [ ] Analytics and usage statistics
- [ ] Docker containerization

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**NISHU KUMAR**

- [LinkedIn](https://www.linkedin.com/in/nishu73/)
- [GitHub](https://github.com/NISHU8875)
- [Portfolio](https://codebasics.io/portfolio/NISHU-KUMAR)

---

## 🔗 Live Demo

**Try it out**: [Open Streamlit App](https://market-research-assistant-nishu-pixii.streamlit.app/)

---

## ❓ FAQ

**Q: Can I use this for my own documents?**
A: Yes! Any publicly accessible URL works. For private documents, you'll need to modify WebBaseLoader.

**Q: How accurate are the responses?**
A: Accuracy depends on document quality and specificity of queries. The LLM is grounded in your documents to minimize hallucination.

**Q: Can I change the LLM model?**
A: Yes, modify the `model` parameter in `rag.py` line 23. Groq supports various models.

**Q: How much does it cost?**
A: Groq offers free API tier with generous limits. Check [groq.com](https://groq.com) for pricing.

**Q: Can I deploy this?**
A: Yes! Deploy to Streamlit Cloud, AWS, GCP, or any Python-compatible platform. See [Streamlit Deployment Docs](https://docs.streamlit.io/deploy/streamlit-cloud).

---

## 🎯 Support

For issues, questions, or suggestions:
- Open a GitHub issue
- Check existing documentation
- Review the troubleshooting section

---

**Last Updated**: May 2026  
**Version**: 2.0.0 (with Prompt Engineering & Web Search)
