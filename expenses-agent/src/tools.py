import requests
from os import environ
from typing import Optional

EXPENSES_API_URL = environ['EXPENSES_API_URL']

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