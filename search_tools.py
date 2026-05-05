"""
Internet Search Tools Module
Provides web search capabilities while prioritizing document-based information
"""

from typing import List, Dict, Tuple, Optional
from langchain_core.tools import tool
import os

# Try to import DuckDuckGo search, fall back to a basic implementation
try:
    from langchain_community.tools import DuckDuckGoSearchRun
    HAS_DUCKDUCKGO = True
except ImportError:
    HAS_DUCKDUCKGO = False

class WebSearchManager:
    """Manages web searches with grounding in document context"""
    
    def __init__(self):
        self.search_enabled = HAS_DUCKDUCKGO
        if self.search_enabled:
            self.search_tool = DuckDuckGoSearchRun()
    
    def search(self, query: str, max_results: int = 3) -> Optional[str]:
        """
        Perform a web search
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            Search results as string or None if search not available
        """
        if not self.search_enabled:
            return None
        
        try:
            results = self.search_tool.run(query)
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return None
    
    def is_search_available(self) -> bool:
        """Check if web search is available"""
        return self.search_enabled
    
    def format_search_results(self, results: str) -> str:
        """Format search results for display"""
        return f"**Web Search Results:**\n{results}"

class GroundedResponseGenerator:
    """
    Generates responses grounded in document context with optional web search
    Prioritizes document information and clearly separates external knowledge
    """
    
    def __init__(self, vector_store_results: List[Dict]):
        """
        Initialize with vector store retrieval results
        
        Args:
            vector_store_results: List of document chunks retrieved from vector store
        """
        self.document_results = vector_store_results
        self.document_sources = self._extract_sources()
    
    def _extract_sources(self) -> set:
        """Extract unique sources from document results"""
        sources = set()
        for result in self.document_results:
            if hasattr(result, 'metadata') and 'source' in result.metadata:
                sources.add(result.metadata['source'])
        return sources
    
    def should_search_web(self, query: str, document_confidence: float = 0.5) -> bool:
        """
        Determine if web search should be performed
        
        Args:
            query: User query
            document_confidence: Confidence score in document results (0-1)
            
        Returns:
            True if web search should be performed
        """
        # Search the web if:
        # 1. Confidence in documents is low
        # 2. Query asks for current/latest information
        # 3. Query involves external verification
        
        current_info_keywords = ['latest', 'recent', 'current', 'today', 'now', '2024', '2025', '2026']
        verification_keywords = ['verify', 'confirm', 'check', 'validate', 'is it true']
        
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in current_info_keywords + verification_keywords):
            return True
        
        if document_confidence < 0.3:
            return True
        
        return False
    
    def generate_grounded_response_prompt(self, 
                                         query: str, 
                                         context: str,
                                         web_results: Optional[str] = None,
                                         use_search: bool = False) -> str:
        """
        Generate a prompt that ensures grounded responses
        
        Args:
            query: User query
            context: Retrieved document context
            web_results: Optional web search results
            use_search: Whether search was used
            
        Returns:
            Formatted prompt for the LLM
        """
        prompt = f"""Based on the provided documents and instructions, answer the following query.

IMPORTANT GROUNDING RULES:
1. PRIMARY SOURCE: Answer primarily using the provided document context
2. EXTERNAL KNOWLEDGE: You may supplement with external knowledge only when:
   - It directly supports or clarifies document information
   - It provides relevant context that doesn't contradict documents
3. CITATION: Always cite which information comes from documents vs. external sources
4. HONESTY: If information is not in documents and cannot be reliably supplemented, say so
5. NO HALLUCINATION: Never make up facts or figures not in documents
6. STRUCTURE: Use tables for comparative data when appropriate

DOCUMENT CONTEXT (PRIMARY SOURCE):
{context}
"""
        
        if use_search and web_results:
            prompt += f"""
SUPPLEMENTARY WEB SEARCH RESULTS (Use to supplement, not replace documents):
{web_results}

Note: Prioritize document information. Use web results only to supplement or verify.
"""
        
        prompt += f"""
USER QUERY:
{query}

RESPONSE INSTRUCTIONS:
- Start with document-based answer
- Clearly label any external information as "Additional context from search:"
- Use markdown tables for structured comparisons
- Cite specific document sources
- If no relevant information found, state clearly

ANSWER:"""
        
        return prompt

def create_grounded_analysis(
    query: str,
    context: str,
    web_results: Optional[str] = None,
    include_search_note: bool = False
) -> Tuple[str, List[str]]:
    """
    Create an analysis prompt and citation guidance
    
    Args:
        query: User query
        context: Document context
        web_results: Optional web search results
        include_search_note: Whether to include search usage note
        
    Returns:
        Tuple of (analysis_prompt, citation_guidelines)
    """
    
    citation_guidelines = [
        "Start with document sources",
        "Mark external information clearly",
        "Use document citations in format: [Source: document_url]",
        "Include data verification when using external sources",
        "Flag any contradictions between sources"
    ]
    
    if include_search_note:
        citation_guidelines.append("Note web search sources separately with [Web Search]")
    
    generator = GroundedResponseGenerator([])
    prompt = generator.generate_grounded_response_prompt(
        query=query,
        context=context,
        web_results=web_results,
        use_search=bool(web_results)
    )
    
    return prompt, citation_guidelines
