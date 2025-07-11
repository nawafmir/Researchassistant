# import streamlit as st
# from streamlit_chat import message
# from dotenv import load_dotenv
# from pydantic import BaseModel
# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import PydanticOutputParser
# from Tools import search_tool
# import re
# import json

# # Page configuration and styling
# st.set_page_config(
#     page_title="Research Assistant",
#     page_icon="🔍",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS
# st.markdown("""
# <style>
#     .stApp {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#     }
#     .main > div {
#         padding: 2rem;
#         border-radius: 1rem;
#         background-color: rgba(255, 255, 255, 0.95);
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#     }
#     .stMarkdown p {
#         font-size: 1.1rem;
#         line-height: 1.6;
#     }
#     .stSpinner > div {
#         text-align: center;
#         padding: 1rem;
#         border-radius: 0.5rem;
#         background-color: rgba(255, 255, 255, 0.9);
#     }
#     div[data-testid="stToolbar"] {
#         display: none;
#     }
#     .stChatMessage {
#         background-color: white;
#         border-radius: 1rem;
#         padding: 1rem;
#         margin: 0.5rem 0;
#         box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
#     }
#     .stChatMessage [data-testid="StyledTheme"] {
#         border-radius: 0.5rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# load_dotenv()

# class ResearchResponse(BaseModel):
#     topic: str
#     summary: str
#     sources: list[str]
#     tools_used: list[str]

# # Initialize Streamlit state
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []

# # Sidebar
# with st.sidebar:
#     st.image("https://raw.githubusercontent.com/streamlit/streamlit/develop/lib/streamlit/static/media/streamlit-mark-color.png", width=100)
#     st.title("Research Assistant")
#     st.markdown("""---
#     👋 Welcome to your AI-powered research companion!
    
#     This tool helps you:
#     - 📚 Research any topic
#     - 🔍 Find reliable sources
#     - 📝 Get structured summaries
#     ---
#     """)
    
#     # Add a clear chat button
#     if st.button("🗑️ Clear Chat History", type="secondary"):
#         st.session_state.chat_history = []
#         st.rerun()

# # Main content area
# st.markdown("<h1 style='text-align: center; color: #1E3D59;'>🔍 Research Assistant</h1>", unsafe_allow_html=True)
# st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #666;'>Ask me anything, and I will help you research it!</p>", unsafe_allow_html=True)

# # Initialize components
# llm = ChatGroq(model="llama3-8b-8192")
# parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# # Prompt templates
# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             """You are a research assistant. If you need to use any tool, tell the user what tool you want.
# "Only say 'search: <your search term>' if you want to search the web."
# {format_instructions}""",
#         ),
#         ("human", "{query}"),
#     ]
# ).partial(format_instructions=parser.get_format_instructions())

# def extract_json(text: str) -> str:
#     """Extract first JSON object from text block."""
#     match = re.search(r"\{.*\}", text, re.DOTALL)
#     if not match:
#         raise ValueError("No JSON object found in model response.")
#     return match.group(0)

# def process_query(query: str):
#     # Step 1: Initial response
#     initial_response = llm.invoke(prompt.format(query=query))
    
#     # Step 2: Check if model wants to use a tool
#     search_match = re.search(r"search\s*:\s*(.+)", initial_response.content, re.IGNORECASE)
    
#     tool_output = ""
#     tools_used = []
#     sources = []
    
#     if search_match:
#         keyword = search_match.group(1).strip()
#         with st.spinner(f'🔍 Searching for \'{keyword}\'...'):
#             tool_output = search_tool.run(keyword)
#             tools_used.append("search")
#             sources.append("DuckDuckGo")

#         # Step 3: Feed tool result back to LLM
#         follow_up_prompt = ChatPromptTemplate.from_messages(
#         [
#             ("system", "Use this tool output to answer the user's query. Wrap in this JSON format:\n{format_instructions}"),
#             ("human", "User asked: {query}\n\nTool output:\n{tool_output}")
#         ]
#         ).partial(format_instructions=parser.get_format_instructions())

#         final_response = llm.invoke(follow_up_prompt.format(query=query, tool_output=tool_output))
#         final_text = final_response.content
#     else:
#         final_text = initial_response.content

#     # Step 4: Parse into structured response
#     try:
#         json_text = extract_json(final_text)
#         structured = parser.parse(json_text)
#         if tools_used:
#             structured.tools_used = tools_used
#             structured.sources = sources
#         return structured
#     except Exception as e:
#         st.error(f"Error parsing response: {e}")
#         st.code(final_text, language="json")
#         return None

# # Create two columns for chat display and input
# col1, col2 = st.columns([3, 1])

# with col1:
#     # Display chat history in a container with custom styling
#     chat_container = st.container()
#     with chat_container:
#         for i, chat in enumerate(st.session_state.chat_history):
#             if chat["role"] == "user":
#                 message(chat["content"], is_user=True, key=f"user_{i}", avatar_style="identicon")
#             else:
#                 message(chat["content"], key=f"assistant_{i}", avatar_style="bottts")

# with col2:
#     st.markdown("### Quick Topics")
#     example_topics = [
#         "Latest AI developments",
#         "Climate change solutions",
#         "Space exploration",
#         "Renewable energy"
#     ]
#     for topic in example_topics:
#         if st.button(f"🔍 {topic}", key=topic, use_container_width=True):
#             user_query = topic
#             st.session_state.chat_history.append({"role": "user", "content": user_query})
#             with st.spinner('Researching...'):
#                 response = process_query(user_query)
#             if response:
#                 assistant_response = f"📝 **Topic**: {response.topic}\n\n{response.summary}"
#                 if response.sources:
#                     assistant_response += f"\n\n🔍 **Sources**: {', '.join(response.sources)}"
#                 st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
#             st.rerun()

# # Chat input at the bottom
# user_query = st.chat_input("What would you like to research?")

# if user_query:
#     # Add user message to chat history
#     st.session_state.chat_history.append({"role": "user", "content": user_query})
    
#     # Process the query
#     with st.spinner('Researching...'):
#         response = process_query(user_query)
    
#     if response:
#         # Format assistant response
#         assistant_response = f"📝 **Topic**: {response.topic}\n\n{response.summary}"
#         if response.sources:
#             assistant_response += f"\n\n🔍 **Sources**: {', '.join(response.sources)}"
        
#         # Add assistant response to chat history
#         st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
#         st.rerun()
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from Tools import search_tool
import re
import json

# Page configuration and styling
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with improved layout
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    .main > div {
        padding: 2rem;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(15px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin: 1rem;
    }
    
    /* Enhanced Chat Input Styling */
    .stChatInput > div {
        background: white !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
        border: 3px solid #3b82f6 !important;
        margin: 2rem 0 !important;
        padding: 0.5rem !important;
        min-height: 70px !important;
    }
    
    .stChatInput input {
        color: #111827 !important;
        background: transparent !important;
        border: none !important;
        font-size: 1.2rem !important;
        padding: 1rem 1.5rem !important;
        min-height: 50px !important;
        line-height: 1.6 !important;
    }
    
    .stChatInput input::placeholder {
        color: #6b7280 !important;
        font-size: 1.1rem !important;
    }
    
    .stChatInput button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 0.8rem 1.2rem !important;
        color: white !important;
        font-weight: 600 !important;
        margin-right: 0.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatInput button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Enhanced Message Styling */
    .user-message {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white !important;
        border-radius: 20px 20px 5px 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
        max-width: 85%;
        margin-left: auto;
        margin-right: 0;
    }
    
    .assistant-message {
        background: white;
        color: #1f2937 !important;
        border-radius: 20px 20px 20px 5px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        max-width: 85%;
        margin-left: 0;
        margin-right: auto;
    }
    
    .research-summary {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 5px solid #3b82f6;
        line-height: 1.8;
        font-size: 1.05rem;
    }
    
    .research-summary h3 {
        color: #1e293b !important;
        margin-bottom: 1rem;
        font-size: 1.4rem;
        font-weight: 600;
    }
    
    .research-summary p {
        color: #374151 !important;
        margin: 1rem 0;
    }
    
    .sources-section {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #10b981;
    }
    
    .sources-section h4 {
        color: #065f46 !important;
        margin-bottom: 0.8rem;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .sources-section p {
        color: #047857 !important;
        font-weight: 500;
        margin: 0.5rem 0;
    }
    
    /* Welcome Section */
    .welcome-section {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-radius: 25px;
        padding: 3rem;
        margin: 2rem 0;
        border: 2px solid #bae6fd;
        text-align: center;
    }
    
    .welcome-section h2 {
        color: #0c4a6e !important;
        margin-bottom: 1.5rem;
        font-weight: 700;
        font-size: 2.2rem;
    }
    
    .welcome-section p {
        color: #164e63 !important;
        font-size: 1.2rem;
        margin: 1rem 0;
        line-height: 1.7;
    }
    
    /* Sidebar Styling */
    .stSidebar {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
    }
    
    .sidebar-header {
        text-align: center;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .sidebar-logo {
        width: 100px;
        height: 100px;
        margin: 0 auto 1rem;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .feature-card h4 {
        color: white !important;
        margin-bottom: 1.5rem;
        font-weight: 600;
        font-size: 1.3rem;
    }
    
    .feature-card p, .feature-card li {
        color: white !important;
        font-weight: 500;
        margin: 0.8rem 0;
        line-height: 1.6;
    }
    
    /* Topic Buttons */
    .topic-button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white !important;
        border: none;
        border-radius: 15px;
        padding: 1rem 1.5rem;
        margin: 0.8rem 0;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(16, 185, 129, 0.3);
        width: 100%;
        text-align: left;
        font-size: 1rem;
    }
    
    .topic-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4);
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
    }
    
    /* Main Header */
    .main-header {
        text-align: center;
        color: #111827 !important;
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-subtitle {
        text-align: center;
        font-size: 1.5rem;
        color: #4b5563 !important;
        margin-bottom: 3rem;
        font-weight: 500;
    }
    
    /* Input Section Header */
    .input-section-header {
        text-align: center;
        margin: 3rem 0 2rem 0;
        padding: 2rem;
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        border-radius: 20px;
        border: 2px solid #e5e7eb;
    }
    
    .input-section-header h3 {
        color: #111827 !important;
        margin: 0;
        font-size: 1.8rem;
        font-weight: 600;
    }
    
    .input-section-header p {
        color: #6b7280 !important;
        margin: 0.8rem 0 0 0;
        font-size: 1.2rem;
    }
    
    /* Error Message Styling */
    .error-message {
        background: #fee2e2;
        border: 1px solid #fecaca;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #dc2626 !important;
        font-weight: 500;
        display: none;
    }
    
    /* Spinner Styling */
    .stSpinner > div {
        text-align: center;
        padding: 2rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white !important;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white !important;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280 !important;
        padding: 3rem;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        margin-top: 3rem;
    }
    
    .footer p {
        color: #6b7280 !important;
        margin: 0.8rem 0;
        font-size: 1.1rem;
    }
    
    /* Hide default Streamlit elements */
    div[data-testid="stToolbar"] {
        display: none;
    }
    
    .stMarkdown p {
        font-size: 1.1rem;
        line-height: 1.7;
        color: #1f2937 !important;
        font-weight: 400;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #111827 !important;
        font-weight: 600;
    }
    
    .stSidebar .stMarkdown p {
        color: white !important;
        font-weight: 500;
    }
    
    .stSidebar .stMarkdown h1, 
    .stSidebar .stMarkdown h2, 
    .stSidebar .stMarkdown h3, 
    .stSidebar .stMarkdown h4, 
    .stSidebar .stMarkdown h5, 
    .stSidebar .stMarkdown h6 {
        color: white !important;
        font-weight: 600;
    }
    
    .stSidebar .stMarkdown li {
        color: white !important;
        font-weight: 400;
    }
</style>
""", unsafe_allow_html=True)

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str] = []
    tools_used: list[str] = []

# Initialize Streamlit state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Enhanced Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-logo">🔬</div>
        <h2 style="margin: 0; font-size: 1.8rem; color: white;">Research Assistant</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; color: white;">AI-Powered Research Companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>🎯 Features</h4>
        <ul style="margin: 0; padding-left: 2rem;">
            <li>📚 Deep research on any topic</li>
            <li>🔍 Find reliable sources</li>
            <li>📝 Comprehensive summaries</li>
            <li>⚡ Real-time web search</li>
            <li>🎨 Beautiful user interface</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.3); margin: 2rem 0;'>", unsafe_allow_html=True)
    
    if st.button("🗑️ Clear Chat History", type="secondary", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.3); margin: 2rem 0;'>", unsafe_allow_html=True)
    
    # Statistics section
    st.markdown(f"""
    <div class="feature-card">
        <h4>📊 Session Stats</h4>
        <p>💬 Total Messages: {len(st.session_state.chat_history)}</p>
        <p>🔍 Research Queries: {len([msg for msg in st.session_state.chat_history if msg.get('role') == 'user'])}</p>
        <p>📝 Responses Generated: {len([msg for msg in st.session_state.chat_history if msg.get('role') == 'assistant'])}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.3); margin: 2rem 0;'>", unsafe_allow_html=True)
    
    # Quick Topics Section
    st.markdown("""
    <div class="feature-card">
        <h4>🚀 Quick Research Topics</h4>
        <p>Click any topic below to start exploring</p>
    </div>
    """, unsafe_allow_html=True)
    
    example_topics = [
        ("🤖 AI Developments", "latest artificial intelligence trends"),
        ("🌍 Climate Solutions", "climate change solutions"),
        ("🚀 Space Exploration", "space exploration news"),
        ("💊 Medical Research", "medical breakthroughs"),
        ("💰 Cryptocurrency", "cryptocurrency trends"),
        ("🔬 Quantum Computing", "quantum computing advances"),
        ("🌱 Green Technology", "sustainable technology"),
        ("📱 Mobile Tech", "mobile technology trends")
    ]
    
    for topic_display, topic_query in example_topics:
        if st.button(topic_display, key=topic_query, use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": topic_query})
            st.rerun()

# Main content area
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 class="main-header">🔬 AI Research Assistant</h1>
    <p class="main-subtitle">Ask me anything, and I'll provide comprehensive research with reliable sources!</p>
</div>
""", unsafe_allow_html=True)

# Initialize components
llm = ChatGroq(model="llama3-8b-8192")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Improved prompt template with better JSON handling
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert research assistant. 
            If you need to search for information, respond with: "SEARCH: <your search term>"
            Otherwise, provide a direct answer.
            
            When providing research responses, structure them as comprehensive summaries with:
            - Clear introduction and context
            - Key findings with detailed explanations
            - Supporting evidence and examples
            - Conclusions and implications
            
            Always maintain a professional and informative tone."""
        ),
        ("human", "{query}"),
    ]
)

def safe_process_query(query: str):
    """Process query with better error handling and cleaner output"""
    try:
        # Step 1: Get initial response
        initial_response = llm.invoke(prompt.format(query=query))
        
        # Step 2: Check if search is needed
        if initial_response.content.startswith("SEARCH:"):
            search_term = initial_response.content.replace("SEARCH:", "").strip()
            
            # Perform search
            with st.spinner(f'🔍 Searching for information about "{search_term}"...'):
                search_results = search_tool.run(search_term)
            
            # Generate comprehensive response with search results
            follow_up_prompt = ChatPromptTemplate.from_messages([
                ("system", """Based on the search results provided, create a comprehensive research summary about the user's query.
                Structure your response with:
                1. Introduction and overview
                2. Key findings and main points
                3. Supporting details and evidence
                4. Recent developments or trends
                5. Conclusion and implications
                
                Make the response informative, well-organized, and engaging.
                Focus on providing valuable insights rather than just listing information."""),
                ("human", "Query: {query}\n\nSearch Results:\n{search_results}")
            ])
            
            final_response = llm.invoke(follow_up_prompt.format(query=query, search_results=search_results))
            
            # Create structured response
            research_data = ResearchResponse(
                topic=query.title(),
                summary=final_response.content,
                sources=["Web Search Results", "Real-time Information"],
                tools_used=["Web Search", "Language Model Analysis"]
            )
            
        else:
            # Direct response without search
            research_data = ResearchResponse(
                topic=query.title(),
                summary=initial_response.content,
                sources=["Knowledge Base"],
                tools_used=["Language Model Analysis"]
            )
        
        return research_data
        
    except Exception as e:
        st.error(f"❌ Error processing query: {str(e)}")
        return None

# Display chat history
if not st.session_state.chat_history:
    st.markdown("""
    <div class="welcome-section">
        <h2>👋 Welcome to Your Advanced Research Assistant!</h2>
        <p>I'm here to help you conduct comprehensive research on any topic. Ask me anything and I'll provide detailed, well-researched information with reliable sources.</p>
        
        <p><strong>🚀 What can I help you research today?</strong></p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 2rem;">
            <div style="background: rgba(59, 130, 246, 0.1); padding: 1.5rem; border-radius: 15px; border: 1px solid rgba(59, 130, 246, 0.2);">
                <h4 style="color: #1e40af; margin: 0 0 0.5rem 0;">🔬 Scientific Research</h4>
                <p style="color: #1e40af; margin: 0; font-size: 0.95rem;">Latest discoveries and breakthroughs</p>
            </div>
            <div style="background: rgba(16, 185, 129, 0.1); padding: 1.5rem; border-radius: 15px; border: 1px solid rgba(16, 185, 129, 0.2);">
                <h4 style="color: #047857; margin: 0 0 0.5rem 0;">📈 Market Analysis</h4>
                <p style="color: #047857; margin: 0; font-size: 0.95rem;">Business trends and insights</p>
            </div>
            <div style="background: rgba(245, 158, 11, 0.1); padding: 1.5rem; border-radius: 15px; border: 1px solid rgba(245, 158, 11, 0.2);">
                <h4 style="color: #92400e; margin: 0 0 0.5rem 0;">🌍 Global Events</h4>
                <p style="color: #92400e; margin: 0; font-size: 0.95rem;">Current developments and news</p>
            </div>
            <div style="background: rgba(139, 92, 246, 0.1); padding: 1.5rem; border-radius: 15px; border: 1px solid rgba(139, 92, 246, 0.2);">
                <h4 style="color: #5b21b6; margin: 0 0 0.5rem 0;">💡 Technology</h4>
                <p style="color: #5b21b6; margin: 0; font-size: 0.95rem;">Innovation and tech trends</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Display existing chat messages
for i, chat in enumerate(st.session_state.chat_history):
    if chat["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            <strong>🙋‍♂️ Your Research Question:</strong><br>
            {chat["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-message">
            <strong>🤖 Research Assistant:</strong>
            {chat["content"]}
        </div>
        """, unsafe_allow_html=True)

# Enhanced input section
st.markdown("""
<div class="input-section-header">
    <h3>💬 Ask Your Research Question</h3>
    <p>Type your question below and get comprehensive research results</p>
</div>
""", unsafe_allow_html=True)

# Chat input
user_query = st.chat_input("🔍 What would you like to research today? (e.g., 'Tell me about artificial intelligence', 'Climate change solutions', 'Space exploration news')")

if user_query:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    
    # Process the query
    research_result = safe_process_query(user_query)
    
    if research_result:
        # Format the response
        formatted_response = f"""
        <div class="research-summary">
            <h3>📋 Research Topic: {research_result.topic}</h3>
            <div style="line-height: 1.8; color: #374151;">
                {research_result.summary.replace('\n', '<br>')}
            </div>
        </div>
        
        <div class="sources-section">
            <h4>🔍 Sources Used:</h4>
            <p>{' • '.join(research_result.sources)}</p>
        </div>
        
        <div class="sources-section">
            <h4>🛠️ Research Tools Used:</h4>
            <p>{' • '.join(research_result.tools_used)}</p>
        </div>
        """
        
        st.session_state.chat_history.append({"role": "assistant", "content": formatted_response})
    
    st.rerun()

# Enhanced Footer
st.markdown("""
<div class="footer">
    <p style="font-size: 1.2rem; font-weight: 600;">🔬 AI Research Assistant</p>
    <p style="font-size: 1rem;">Powered by Advanced Language Models • Enhanced with Modern Design</p>
    <p style="font-size: 0.95rem; margin-top: 1rem;">Built with Streamlit • Designed for Comprehensive Research</p>
</div>
""", unsafe_allow_html=True)