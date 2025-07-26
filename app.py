import streamlit as st
import google.generativeai as ai
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Chatbot Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white !important;
        margin: 0;
    }
    
    .main-header p {
        color: white !important;
        margin: 0;
    }
    
    .chat-message-user {
        background-color: #e3f2fd !important;
        color: #000000 !important;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border: 2px solid #2196f3;
        text-align: left;
    }
    
    .chat-message-bot {
        background-color: #f5f5f5 !important;
        color: #000000 !important;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border: 2px solid #4caf50;
        text-align: left;
    }
    
    .message-text {
        color: #000000 !important;
        font-size: 14px;
        line-height: 1.5;
    }
    
    .message-label {
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .user-label {
        color: #1976d2 !important;
    }
    
    .bot-label {
        color: #388e3c !important;
    }
    
    .message-avatar {
        width: 35px;
        height: 35px;
        border-radius: 50%;
        margin-right: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        flex-shrink: 0;
    }
    
    .user-avatar {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
        color: white;
    }
    
    .bot-avatar {
        background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%);
        color: white;
    }
    
    .message-content {
        flex: 1;
        line-height: 1.5;
    }
    
    .input-container {
        position: sticky;
        bottom: 0;
        background: white;
        padding: 1rem 0;
        border-top: 1px solid #e0e0e0;
        margin-top: 1rem;
    }
    
    .quick-actions {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #dee2e6;
        text-align: center;
    }
    
    .error-message {
        background-color: #ffebee;
        color: #c62828;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ef5350;
        margin: 1rem 0;
    }
    
    .success-message {
        background-color: #e8f5e8;
        color: #2e7d32;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #4caf50;
        margin: 1rem 0;
    }
    
    /* Hide Streamlit's default elements */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'model_settings' not in st.session_state:
        st.session_state.model_settings = {
            'temperature': 0.7,
            'max_tokens': 1000,
            'model_name': 'gemini-2.0-flash'
        }
    if 'chat_input' not in st.session_state:
        st.session_state.chat_input = ""

initialize_session_state()

# Initialize AI model
@st.cache_resource
def initialize_model():
    try:
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            st.error("⚠️ API_KEY not found in environment variables. Please check your .env file.")
            return None
        
        ai.configure(api_key=API_KEY)
        return ai.GenerativeModel("gemini-2.0-flash")
    except Exception as e:
        st.error(f"Error initializing model: {str(e)}")
        return None

# Function to generate AI response
def generate_response(user_input, model):
    try:
        # Create generation config
        generation_config = ai.types.GenerationConfig(
            temperature=st.session_state.model_settings['temperature'],
            max_output_tokens=st.session_state.model_settings['max_tokens']
        )
        
        # Build conversation context
        context = ""
        if len(st.session_state.messages) > 1:
            # Include last few messages for context (limit to prevent token overflow)
            recent_messages = st.session_state.messages[-6:]  # Last 6 messages
            for msg in recent_messages:
                role = "Human" if msg["role"] == "user" else "Assistant"
                context += f"{role}: {msg['content']}\n"
        
        # Add current input
        full_prompt = f"{context}Human: {user_input}\nAssistant:"
        
        # Generate response
        response = model.generate_content(
            full_prompt,
            generation_config=generation_config
        )
        
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Sidebar
with st.sidebar:
    st.markdown("## 🛠️ Settings")
    
    # Model settings
    st.markdown("### Model Configuration")
    temperature = st.slider(
        "Temperature", 
        0.0, 2.0, 
        st.session_state.model_settings['temperature'], 
        0.1,
        help="Controls randomness in responses. Higher values = more creative."
    )
    max_tokens = st.slider(
        "Max Tokens", 
        100, 2000, 
        st.session_state.model_settings['max_tokens'], 
        100,
        help="Maximum length of the response."
    )
    
    # Update settings
    st.session_state.model_settings.update({
        'temperature': temperature,
        'max_tokens': max_tokens
    })
    
    st.markdown("---")
    
    # Chat management
    st.markdown("### 💬 Chat Management")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_input = ""
            st.rerun()
    
    with col2:
        if st.button("💾 Save", use_container_width=True):
            if st.session_state.messages:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                chat_data = {
                    'timestamp': timestamp,
                    'messages': st.session_state.messages,
                    'settings': st.session_state.model_settings
                }
                st.session_state.chat_history.append(chat_data)
                st.success("✅ Chat saved!")
            else:
                st.warning("⚠️ No messages to save!")
    
    # Export functionality
    if st.session_state.messages:
        st.markdown("### 📤 Export Options")
        
        # Prepare export data
        chat_json = json.dumps(st.session_state.messages, indent=2)
        chat_text = ""
        for message in st.session_state.messages:
            role = "You" if message["role"] == "user" else "Assistant"
            chat_text += f"{role}: {message['content']}\n\n"
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📋 JSON",
                data=chat_json,
                file_name=f"chat_{timestamp}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            st.download_button(
                label="📄 Text",
                data=chat_text,
                file_name=f"chat_{timestamp}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    # Statistics
    st.markdown("### 📊 Statistics")
    total_messages = len(st.session_state.messages)
    user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
    bot_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total", total_messages)
    with col2:
        st.metric("You", user_messages)
    with col3:
        st.metric("Bot", bot_messages)

# Main content
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Chatbot Assistant</h1>
    <p>Powered by Google Gemini AI • Smart • Responsive • Helpful</p>
</div>
""", unsafe_allow_html=True)

# Quick actions
st.markdown("### 🚀 Quick Actions")
col1, col2, col3, col4 = st.columns(4)

quick_prompts = {
    "💡 Ideas": "Give me some creative ideas for a project",
    "📝 Writing": "Help me improve my writing skills",
    "🧮 Math": "Help me solve a math problem",
    "🌟 Fun Facts": "Tell me an interesting fun fact"
}

for i, (col, (label, prompt)) in enumerate(zip([col1, col2, col3, col4], quick_prompts.items())):
    with col:
        if st.button(label, use_container_width=True, key=f"quick_{i}"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

# Chat interface
st.markdown("### 💬 Chat")

# Display chat messages
if st.session_state.messages:
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            # User message - right aligned
            col1, col2 = st.columns([1, 4])
            with col2:
                st.markdown(f"""
                <div style="background-color: #e3f2fd; color: #000000; 
                            padding: 15px; border-radius: 15px; margin: 10px 0;
                            border: 2px solid #2196f3; text-align: left;">
                    <strong style="color: #1976d2;">👤 You:</strong><br>
                    <span style="color: #000000;">{message["content"]}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Bot message - left aligned
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div style="background-color: #f5f5f5; color: #000000; 
                            padding: 15px; border-radius: 15px; margin: 10px 0;
                            border: 2px solid #4caf50; text-align: left;">
                    <strong style="color: #388e3c;">🤖 Assistant:</strong><br>
                    <span style="color: #000000;">{message["content"]}</span>
                </div>
                """, unsafe_allow_html=True)
else:
    st.info("👋 Welcome! Start a conversation by typing a message below or use the quick actions above.")

# Chat input section
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Message",
            placeholder="Type your message here... (Press Enter to send)",
            label_visibility="collapsed",
            key="message_input"
        )
    
    with col2:
        send_button = st.form_submit_button("Send 🚀", use_container_width=True)

# Handle user input
if send_button and user_input.strip():
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    
    # Generate response
    with st.spinner("🤔 Thinking..."):
        model = initialize_model()
        if model:
            response_text = generate_response(user_input.strip(), model)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        else:
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "Sorry, I'm having trouble connecting to the AI service. Please check your API configuration."
            })
    
    st.rerun()

# Footer with sample prompts
with st.expander("💡 Sample Prompts to Get Started"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎨 Creative & Fun:**
        - Write a short story about time travel
        - Create a poem about technology
        - Tell me a joke
        - Create a riddle for me to solve
        
        **📚 Learning & Education:**
        - Explain quantum computing simply
        - Teach me about machine learning
        - What are the benefits of renewable energy?
        - Help me understand calculus
        """)
    
    with col2:
        st.markdown("""
        **💻 Technical Help:**
        - Help me debug this Python code
        - Explain REST APIs
        - Best practices for web development
        - How to optimize database queries
        
        **💼 Professional:**
        - Help me write a professional email
        - Create a project plan template
        - Tips for effective presentations
        - Career advice for developers
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🤖 <strong>AI Chatbot Assistant</strong> | Built with ❤️ using Streamlit & Google Gemini AI</p>
    <p><small>💡 Tip: Use the sidebar to customize settings, export chats, and view statistics!</small></p>
</div>
""", unsafe_allow_html=True)