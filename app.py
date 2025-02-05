import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)
st.markdown("""
<style>
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #ffffff;
    }
    
    /* Header styling */
    h1 {
        color: #4ecdc4;
        text-align: center;
        font-size: 2.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Chat message styling */
    .stChatMessage {
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        max-width: 80%;
    }
    
    /* User message styling */
    .stChatMessage[data-testid="user"] {
        background: rgba(78, 205, 196, 0.15);
        border: 1px solid #4ecdc4;
        margin-left: auto;
    }
    
    /* Assistant message styling */
    .stChatMessage[data-testid="assistant"] {
        background: rgba(30, 39, 73, 0.9);
        border: 1px solid #2a3a6e;
        margin-right: auto;
    }
    
    /* Code block styling */
    code {
        background: rgba(0, 0, 0, 0.3) !important;
        color: #4ecdc4 !important;
        padding: 0.2em 0.4em !important;
        border-radius: 3px;
    }
    
    /* Input field styling */
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid #4ecdc4 !important;
        border-radius: 10px;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(45deg, #4ecdc4, #45b7af) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 25px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(78, 205, 196, 0.4);
    }
    
    /* Response text styling */
    .message-content {
        font-size: 1.1em;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)
st.title("Deepseek That Works")
st.caption("As DeepSeek never works it sbetter to use ollama and run it locally")
import streamlit as st

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # Model Selection Dropdown
    selected_model = st.selectbox(
        "Choose Model",
        ["deepseek-r1", "deepseek-r1:7b"],
        index=0
    )

    st.divider()

    # Model Capabilities Section
    st.markdown("### 🚀 Model Capabilities")
    st.markdown("""
    - 🐍 Python Expert  
    - 🛠️ Debugging Assistant  
    - 📄 Code Documentation  
    - 💡 Solution Design  
    """)

    st.divider()

    # Footer with Credits
    st.markdown(
        'Built with [Ollama](https://ollama.ai/) | [LangChain](https://python.langchain.com/)',
        unsafe_allow_html=True
    )
#intititate chat

llm_engine=ChatOllama(
    model=selected_model,
    base_url="http://localhost:11434",
    
    temperature = 0.3
)
system_prompt= SystemMessagePromptTemplate.from_template(
    "You are an expert AI coding assistant. Provide consise, correct solutions"
    "with strategic print statements for debugging coding related problems. Always respond in english"
)

if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role":"ai","content":"Hi!, I am DeepSeek how can i help you code"}]

chat_container = st.container()

with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

user_query = st.chat_input("Type your question here...")

def generate_ai_response(prompt_chain):
    processing_pipeline=prompt_chain | llm_engine | StrOutputParser()
    return processing_pipeline.invoke({})

def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"]=="user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"]=="ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

if user_query:
    st.session_state.message_log.append({"role":"user","content":user_query})

    with st.spinner("Processing..."):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(prompt_chain)
    
    st.session_state.message_log.append({"role":"ai","content":ai_response})
    st.rerun()
