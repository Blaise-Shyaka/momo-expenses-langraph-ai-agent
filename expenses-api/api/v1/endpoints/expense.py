from fastapi import APIRouter, HTTPException, Depends
from schemas.schema import Expense, ExpenseCreate, ExpenseWithCategory, CategoryWithTotal
from db.models import ExpenseDB, CategoryDB
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from api.deps import get_db
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/", response_model=Expense, tags=["Expenses"])
async def create_expense(expense: ExpenseCreate, db: AsyncSession = Depends(get_db)):
    category_stmt = select(CategoryDB).where(func.lower(CategoryDB.name) == expense.category_name.lower())
    result = await db.execute(category_stmt)
    db_category = result.scalars().first()
    if not db_category:
        db_category = CategoryDB(name=expense.category_name)
        db.add(db_category)
        await db.commit()
        await db.refresh(db_category)

    # Create expense
    db_expense = ExpenseDB(
        amount=expense.amount,
        description=expense.description,
        date=expense.date,
        category_id=db_category.id
    )
    db.add(db_expense)
    await db.commit()
    await db.refresh(db_expense)
    return db_expense

@router.get("/{expense_id}", response_model=ExpenseWithCategory, tags=["Expenses"])
async def read_expense(expense_id: int, db: AsyncSession = Depends(get_db)):
    expense_stmt = select(ExpenseDB).options(selectinload(ExpenseDB.category)).where(ExpenseDB.id == expense_id)
    result = await db.execute(expense_stmt)
    expense = result.scalars().first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.get("/", response_model=List[ExpenseWithCategory], tags=["Expenses"])
async def read_expenses(
        skip: int = 0,
        limit: int = 100,
        category_name: Optional[str] = None,
        db: AsyncSession = Depends(get_db)
):
    expense_stmt = select(ExpenseDB).options(selectinload(ExpenseDB.category))
    if category_name:
        expense_stmt = expense_stmt.join(CategoryDB).filter(func.lower(CategoryDB.name) == category_name.lower()).offset(skip).limit(limit)

    result = await db.execute(expense_stmt)
    return result.scalars().all()


@router.get("/totals/by-category", response_model=List[CategoryWithTotal], tags=["Reports"])
async def get_expenses_by_category(db: AsyncSession = Depends(get_db)):
    expense_by_category_stmt = select(CategoryDB, func.sum(ExpenseDB.amount).label("total_expenses")).join(ExpenseDB, CategoryDB.id == ExpenseDB.category_id).group_by(CategoryDB.id)
    # results = (
    #     await db.query(
    #         CategoryDB,
    #         func.sum(ExpenseDB.amount).label("total_expenses")
    #     )
    #     .join(ExpenseDB, CategoryDB.id == ExpenseDB.category_id)
    #     .group_by(CategoryDB.id)
    #     .all()
    # )
    result = await db.execute(expense_by_category_stmt)
    results = result.all()  # Get tuples of (CategoryDB, total)

    return [
        CategoryWithTotal(
            id=category.id,
            name=category.name,
            description=category.description,
            total_expenses=total or 0.0
        )
        for category, total in results
    ]


@router.get("/totals/since", tags=["Reports"])
async def get_expenses_since(
        days: Optional[int] = None,
        start_date: Optional[datetime] = None,
        category_name: Optional[str] = None,
        db: AsyncSession = Depends(get_db)
):
   
    if days is not None and start_date is None:
        start_date = datetime.now() - timedelta(days=days)
    elif start_date is None:
        # Default to last 30 days if neither is provided
        start_date = datetime.now() - timedelta(days=30)

    expense_stmt = select(func.sum(ExpenseDB.amount).label("total")).where(ExpenseDB.date >= start_date)
    
    # Apply category filter if provided
    if category_name:
        expense_stmt = expense_stmt.join(CategoryDB).filter(func.lower(CategoryDB.name) == category_name.lower())

    result = await db.execute(expense_stmt)
    total = result.scalar() or 0.0

    return {
        "start_date": start_date,
        "category": category_name,
        "total_expenses": total
    }