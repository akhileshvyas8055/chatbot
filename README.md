🤖 AI Chatbot Assistant
A beautifully styled, interactive chatbot built with Streamlit and powered by Google Gemini AI. It supports live chatting, customizable AI settings, conversation history export, and a delightful user experience — all from your browser.

📌 Features
🌈 Custom UI Styling for a modern and engaging chat experience

⚙️ Adjustable AI Settings: temperature and max tokens

💬 Live Conversation Interface

📥 Export Options: download your chat history as JSON or plain text

💾 Save Chat and review later

📊 Conversation Statistics: total, user, and bot messages

⚡ Quick Prompt Buttons for instant idea generation

🧠 Context-Aware: includes chat history for better AI responses

✅ Environment-Aware: Warns if API_KEY is missing

🚀 Live Preview
Streamlit app runs in the browser — no HTML/CSS/JS knowledge required!

<p align="center"> <img src="https://user-images.githubusercontent.com/placeholder/ai-chat-preview.png" width="600" alt="Chat UI Preview"/> </p>
🛠️ Setup Instructions
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/ai-chatbot-assistant.git
cd ai-chatbot-assistant
2. Create Environment File
Create a .env file in the root directory and add your Google AI API key:

ini
Copy
Edit
API_KEY=your_google_generative_ai_api_key
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Run the App
bash
Copy
Edit
streamlit run app.py
📂 File Overview
File / Folder	Description
app.py	Main Streamlit chatbot logic
requirements.txt	Python dependencies
.env	Your API key goes here
chat_log.txt	Sample saved chat logs
.gitattributes	Git config for LF normalization

🎨 Interface Highlights
Styled User & Bot Messages

Sticky Chat Input at the bottom of the screen

Sidebar Tools: model tuning, chat clearing, exporting, metrics

Quick Actions: Predefined smart prompts

Responsive & mobile-friendly layout

💡 Sample Prompts
Category	Prompt Example
Creative	"Write a poem about AI in the future"
Educational	"Explain quantum computing simply"
Technical	"Help debug a Python function"
Professional	"Draft a project proposal email"

🧪 Chat Log Example
A snippet from chat_log.txt:

vbnet
Copy
Edit
You: Hi
Chatbot: Hi there! How can I help you today?

You: How is the weather in Aunta, Uttar Pradesh?
Chatbot: Currently, I don't have access to live weather data. Try Google Weather or AccuWeather for real-time info.
📌 Requirements
Python 3.7+

Google Gemini API key

Internet connection

Install dependencies via:

bash
Copy
Edit
pip install streamlit google-generativeai python-dotenv
✨ Future Ideas
🌐 Add live weather and news APIs

📲 Deploy to Streamlit Cloud or Hugging Face Spaces

🧠 Support other AI models (OpenAI, Claude, etc.)

📊 Chat analytics dashboard

🙌 Acknowledgments
Built with ❤️ using:

Streamlit

Google Generative AI SDK

Python Dotenv