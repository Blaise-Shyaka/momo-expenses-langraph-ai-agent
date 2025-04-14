import json
import requests
import os
from typing import TypedDict, List, Optional, Tuple
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

from langgraph.graph import StateGraph, START, END
import google.generativeai as genai

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
llm_model = genai.GenerativeModel('gemini-1.5-flash-latest', generation_config={"response_mime_type": "application/json"})

PROMPT = """
You're an AI Agent responsible for recording a user's expenses. The user will send you a message and you will extract the following information this this message:{message}
Return ONLY JSON with this format:
- amount (float)
- description (str)
- category_name (str)
- date (timestamp)
"""

class ExpenseDetails(BaseModel):
    amount: float = None
    description: str = None
    category_name: str = None
    date: str = datetime.today().timestamp()

class MessageState(TypedDict):
    messages: List[dict]
    expense: ExpenseDetails
    api_response: Optional[dict]

def add_user_message(state: MessageState) -> MessageState:
    return {
        "messages": state["messages"] + [{"role": "user", "content": "Hello, I spent $42.50 on groceries at Whole Foods yesterday"}],
        "expense": ExpenseDetails(),
        "api_response": None
    }

def extract_expense_details(state: MessageState) -> MessageState:
    user_message = state["messages"][-1].get("content")
    llm_model_response = llm_model.generate_content(PROMPT.format(message=user_message))
    print("llm_model_response.text")
    print(llm_model_response.text)
    print(type(llm_model_response.text))

    try:
        parsed_llm_model_response = json.loads(llm_model_response.text)

        return {
                "messages": state["messages"] + [{"role": 'AI Assistant', "content": "Successfully extracted your expenses"}],
                "expense": ExpenseDetails.model_validate(parsed_llm_model_response),
                "api_response": None
            }
    except json.decoder.JSONDecodeError:
        print("Error decoding JSON")
        return {
            "messages": state["messages"] + [{"role": 'AI Assistant', "content": "Failed to extract your expenses. Can you try again?"}],
            "expense": ExpenseDetails(),
            "api_response": None
        }

def record_expense(state: MessageState) -> MessageState:
    expense = state["expense"]

    try:
        response = requests.post(os.environ['EXPENSES_API_URL'], json=expense.model_dump())
        return {
                "messages": state["messages"] + [{"role": 'AI Assistant', "content": "recorded expense successfully"}],
                "expense": expense,
                "api_response": response.json()
            }
    except requests.exceptions.RequestException as e:
        print(e.response.text)
        return {
            "messages": state["messages"],
            "expense": expense,
            "api_response": None
        }

builder = StateGraph(MessageState)
builder.add_node('add_user_message', add_user_message)
builder.add_node('extract_expense_details', extract_expense_details)
builder.add_node('record_expense', record_expense)

builder.set_entry_point("add_user_message")
builder.add_edge('add_user_message', 'extract_expense_details')
builder.add_edge('extract_expense_details', 'record_expense')
builder.add_edge('record_expense', END)

agent = builder.compile()

initial_state = MessageState(messages=[], expense=ExpenseDetails(), api_response=None)
result = agent.invoke(initial_state)
