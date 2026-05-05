import streamlit as st
from rag import process_urls, generate, reset_vector_store, get_available_prompt_templates, get_prompt_template_descriptions, is_web_search_available, set_prompt_template, current_prompt_template

st.set_page_config(page_title="Research Assistant RAG", layout="wide")
st.title("🔍 Market Research Assistant - Pixii :")")

# Initialize session state
if "initialized" not in st.session_state:
    reset_vector_store()
    st.session_state.initialized = True

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")

# Prompt Template Selection
st.sidebar.subheader("📝 Prompt Template")
available_templates = get_available_prompt_templates()
template_descriptions = get_prompt_template_descriptions()

selected_template = st.sidebar.selectbox(
    "Select Response Style:",
    options=available_templates,
    format_func=lambda x: f"{x}: {template_descriptions.get(x, '')}"
)

# Web Search Toggle
st.sidebar.subheader("🌐 Search Options")
use_web_search = st.sidebar.checkbox(
    "Enable Web Search",
    value=False,
    help="Enable supplementary web search for current/external information"
)

# Safely check if web search is available
try:
    web_search_available = is_web_search_available()
except Exception as e:
    web_search_available = False
    print(f"⚠️ Error checking web search availability: {e}")

if not web_search_available:
    st.sidebar.warning("⚠️ Web search not available. Install duckduckgo-search to enable it.")

# URL Processing Section
st.sidebar.subheader("📥 Process URLs")
url1 = st.sidebar.text_input("URL 1")
url2 = st.sidebar.text_input("URL 2")
url3 = st.sidebar.text_input("URL 3")

process_urls_button = st.sidebar.button("🚀 Process URLs", use_container_width=True)

if process_urls_button:
    urls = [url for url in [url1, url2, url3] if url != ""]

    if len(urls) == 0:
        st.error("❌ No URLs entered. Please enter at least one URL to continue.")
    else:
        with st.status("📊 Processing URLs...", expanded=True) as status:
            for url_status in process_urls(urls):
                st.write(url_status)
            status.update(label="✅ Chunks stored! You can now ask questions", expanded=False)

# Display message history
if 'message' not in st.session_state:
    st.session_state['message'] = []

if st.session_state['message']:
    st.subheader("📋 Conversation History")
    for message in st.session_state['message']:
        if message['role'] == 'User':
            with st.chat_message(name='User'):
                st.caption("Query")
                st.markdown(message['query'])
        else:
            with st.chat_message(name='Assistant'):
                st.caption("Solution")
                st.markdown(message['result'])
                
                # Display search info if available
                if 'search_info' in message and message['search_info']:
                    st.info(f"ℹ️ {message['search_info']}")
                
                if 'source' in message:
                    st.caption("Sources")
                    unique_sources = set([message['source']]) if isinstance(message['source'], str) else set(message['source'])
                    for source in unique_sources:
                        st.markdown(f"📎 {source}")

# Main chat interface
st.subheader("💬 Ask a Question")
prompt = st.chat_input("Type your question here...")

# Generate results
if prompt:
    try:
        # Set the selected prompt template
        set_prompt_template(selected_template)
        
        # Determine if web search should be used
        search_flag = use_web_search and web_search_available
        
        # Generate response
        solution, sources, search_info = generate(
            prompt, 
            use_web_search=search_flag,
            prompt_template=selected_template
        )
        
        # Display user query
        with st.chat_message(name="User"):
            st.caption("Query")
            st.markdown(prompt)
        
        st.session_state.message.append({'role': "User", 'query': prompt})
        
        # Display assistant response
        with st.chat_message(name='Assistant'):
            st.caption("Solution")
            st.markdown(solution)
            
            # Display search info if available
            if search_info:
                st.info(f"ℹ️ {search_info}")
            
            if sources:
                st.caption("📚 Sources")
                unique_sources = set(sources)
                for source in unique_sources:
                    st.markdown(f"📎 {source}")
        
        st.session_state.message.append({
            'role': "Assistant",
            'result': solution,
            'source': sources,
            'search_info': search_info,
            'template_used': selected_template
        })
        
        # Rerun to update UI
        st.rerun()

    except RuntimeError as e:
        st.error(f"❌ {str(e)}")