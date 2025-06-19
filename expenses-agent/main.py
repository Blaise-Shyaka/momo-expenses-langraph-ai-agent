import requests
import json
from os import environ
from langgraph.graph import MessagesState, StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from typing import Optional

class ExpensesAgentState(MessagesState):
  pass

EXPENSES_API_URL = environ['EXPENSES_API_URL']

# Let's define tools
def get_all_expenses():
  """It retrieves all expenses a user has recorded.
    The number retrieved is just the first 100 entries.
  """
  url = EXPENSES_API_URL + "/expenses"
  try:
    response = requests.get(url)
    return response.json()
  except requests.exceptions.RequestException as e:
    print(e.response.text)

def create_expense_category(name: str, description: Optional[str]):
  """It creates an new expense category, if it doesn't alread exist. All expenses are recorded under a specific category
    This helps to retrieve and record an expense category.

    Parameters:
      name (str) - The category name
      description (str) - The category description. It is optional.
  """
  url = EXPENSES_API_URL + "/categories"
  payload = { "name": name, "description": description }
  try:
    response = requests.post(url, json=payload)
    return response.json()
  except requests.exceptions.RequestException as e:
    print(e.response.text)

def get_all_categories():
  """It retrieves all categories. It retrieves the first 100 entries."""
  url = EXPENSES_API_URL + "/categories"
  try:
    response = requests.get(url)
    return response.json()
  except requests.exceptions.RequestException as e:
    print(e.response.text)

tools = [get_all_expenses, create_expense_category, get_all_categories]

gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5).bind_tools(tools)
system_message = SystemMessage(content="You are an AI assistant tasked with being and expenses tracker for users. Your name is Reddington. You try to stick to the mission and avoid straying away from it. You have a friendly, playful, and respectful tone.")
messages = [system_message]

def gemini_node(state: ExpensesAgentState):
  return { "messages": gemini_llm.invoke(messages + state["messages"]) }

graph = StateGraph(ExpensesAgentState)

graph.add_node(gemini_node)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "gemini_node")
graph.add_conditional_edges("gemini_node", tools_condition)
graph.add_edge("tools", "gemini_node")
graph.compile()
