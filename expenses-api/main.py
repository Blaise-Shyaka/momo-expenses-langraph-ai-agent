from fastapi import FastAPI
from api.v1.endpoints import category, expense

app = FastAPI(title="Expenses Tracker API")

app.include_router(expense.router, prefix="/api/v1/expenses", tags=["Expenses"])
app.include_router(category.router, prefix="/api/v1/categories", tags=["Categories"])
