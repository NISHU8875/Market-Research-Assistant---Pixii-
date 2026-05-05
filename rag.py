#Importing necessary libs

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from uuid import uuid4
from dotenv import load_dotenv
from prompts_config import get_query_prompt, get_system_prompt, DEFAULT_PROMPT_TEMPLATE
from search_tools import WebSearchManager, GroundedResponseGenerator
from typing import Tuple, List, Optional

load_dotenv()
#Constants
CHUNK_SIZE = 1000
COLLECTION_NAME = "real_estate"
EMBEDDING_MODEL = 'Alibaba-NLP/gte-base-en-v1.5'

#global var
llm = None
vector_store = None
search_manager = None
current_prompt_template = DEFAULT_PROMPT_TEMPLATE

def initialize():
    global llm, vector_store, search_manager
    if llm is None:
        llm = ChatGroq(model='llama-3.3-70b-versatile', temperature=0.7, max_tokens=700)

    if vector_store is None:
        ef = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"trust_remote_code": True}
        )
        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory= './resources/vectorstore',
            embedding_function=ef,
        )
    
    if search_manager is None:
        search_manager = WebSearchManager()

def reset_vector_store():
    global vector_store
    if vector_store is not None:
        vector_store.reset_collection()

def process_urls(urls):
    initialize()
    yield "Loading data from url"
    loader = WebBaseLoader(urls)
    data= loader.load()

    yield "Data loaded, Creating chunks"
    splitter = RecursiveCharacterTextSplitter(
        chunk_size= CHUNK_SIZE,
        separators= ["\n\n","\n","."," "],
        chunk_overlap=200
    )
    docs = splitter.split_documents(data)

    yield "Chunks created, storing in a vector store.."

    if docs:
        uuids = [str (uuid4()) for _ in range(len(docs))]
        vector_store.add_documents(docs,ids = uuids)


def generate(query: str, use_web_search: bool = False, prompt_template: str = DEFAULT_PROMPT_TEMPLATE) -> Tuple[str, List[str], Optional[str]]:
    """
    Generate response based on query and retrieved documents
    
    Args:
        query: User query
        use_web_search: Whether to use web search for supplementary information
        prompt_template: Type of prompt template to use
        
    Returns:
        Tuple of (answer, sources, search_info)
    """
    if not vector_store:
        raise RuntimeError("Vector store not initialized")

    if vector_store._collection.count() == 0:
        raise RuntimeError("No documents found")

    # Retrieve relevant documents
    results = vector_store.similarity_search(
        query,
        k=2,
    )
    sources = [result.metadata['source'] for result in results]
    
    # Format context from retrieved documents
    context = "\n\n".join([f"Document: {result.page_content}\nSource: {result.metadata.get('source', 'Unknown')}" 
                           for result in results])
    
    # Optional: Use web search for supplementary information
    web_results = None
    search_info = None
    if use_web_search and search_manager and search_manager.is_search_available():
        web_results = search_manager.search(query)
        if web_results:
            search_info = "Web search results included for supplementary information"
    
    # Get the appropriate prompt template
    prompt_text = get_query_prompt(prompt_template)
    
    # Create the prompt with context
    prompt = PromptTemplate.from_template(prompt_text)
    
    # Format the prompt with context and query
    if web_results:
        formatted_prompt = prompt_text.format(
            context=context,
            query=query
        ) + f"\n\nWEB SEARCH SUPPLEMENTARY DATA:\n{web_results}"
    else:
        formatted_prompt = prompt_text.format(
            context=context,
            query=query
        )
    
    # Generate response using LLM
    from langchain_core.prompts import ChatPromptTemplate
    system_prompt = get_system_prompt(prompt_template)
    
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", formatted_prompt)
    ])
    
    chain = chat_prompt | llm
    sol = chain.invoke({})
    
    return sol.content, sources, search_info

if __name__ == "__main__":
    pass


# Additional helper functions

def set_prompt_template(template_name: str) -> bool:
    """
    Set the active prompt template
    
    Args:
        template_name: Name of the template to use
        
    Returns:
        True if successful, False otherwise
    """
    global current_prompt_template
    from prompts_config import list_available_templates
    
    if template_name in list_available_templates():
        current_prompt_template = template_name
        return True
    return False

def get_available_prompt_templates() -> List[str]:
    """Get list of available prompt templates"""
    from prompts_config import list_available_templates, get_template_description
    return list_available_templates()

def get_prompt_template_descriptions() -> dict:
    """Get descriptions of all available templates"""
    from prompts_config import get_template_description
    return get_template_description()

def is_web_search_available() -> bool:
    """Check if web search capability is available"""
    initialize()
    return search_manager.is_search_available() if search_manager else False