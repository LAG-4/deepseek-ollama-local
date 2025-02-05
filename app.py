import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # Model Selection Dropdown
    selected_model = st.selectbox(
        "Choose Model",
        ["deepseek-r1", "deepseek-r1:3b"],
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

# CSS Styling for Streamlit UI
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

st.title("Deepseek Code Companion")
st.caption("AI Pair Programmer with Debugging Superpower")

# ✅ Corrected ChatPromptTemplate to avoid KeyError
prompt = ChatPromptTemplate.from_template("""
<style>
    background: {{ background }};
    color: {{ color }};
    font-size: {{ font_size }};
    padding: {{ padding }};
    transform: {{ transform }};
</style>

User: {{ role }}
""")

# 🔹 Pass the required variables
filled_prompt = prompt.format(
    background="white",
    color="black",
    font_size="14px",
    padding="10px",
    transform="none",
    role="developer"
)

# Display the generated prompt in Streamlit
st.markdown(f"### Generated Prompt\n```{filled_prompt}```")

# Initialize AI Model
ai_model = ChatOllama(model=selected_model)
output_parser = StrOutputParser()

# User Input Field
user_input = st.text_input("Enter your query:")

if user_input:
    with st.spinner("Generating response..."):
        response = ai_model.invoke(user_input)  # ✅ FIXED: Using .invoke() instead of .run()
        st.write("### AI Response")
        st.write(response)
