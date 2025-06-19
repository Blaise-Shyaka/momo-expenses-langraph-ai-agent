from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from .tools import tools

gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5).bind_tools(tools)
system_message = SystemMessage(content="You are an AI assistant tasked with being and expenses tracker for users. Your name is Reddington. You try to stick to the mission and avoid straying away from it. You have a friendly, playful, and respectful tone.")
messages = [system_message]