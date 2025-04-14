from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, func, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from typing import List, Optional
from datetime import datetime, timedelta

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./expenses.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database models
class CategoryDB(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)

    expenses = relationship("ExpenseDB", back_populates="category")


class ExpenseDB(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.now)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("CategoryDB", back_populates="expenses")


# Create tables
Base.metadata.create_all(bind=engine)


# Pydantic models for request/response
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class ExpenseBase(BaseModel):
    amount: float
    description: Optional[str] = None
    date: Optional[datetime] = Field(default_factory=datetime.now)


class ExpenseCreate(ExpenseBase):
    category_name: str


class Expense(ExpenseBase):
    id: int
    category_id: int

    class Config:
        from_attributes = True


class ExpenseWithCategory(Expense):
    category: Category

    class Config:
        from_attributes = True


class CategoryWithTotal(Category):
    total_expenses: float


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="Expenses Tracker API")


# Category endpoints
@app.post("/categories/", response_model=Category, tags=["Categories"])
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(CategoryDB).filter(CategoryDB.name == category.name).first()
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")

    db_category = CategoryDB(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@app.get("/categories/", response_model=List[Category], tags=["Categories"])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.query(CategoryDB).offset(skip).limit(limit).all()
    return categories


@app.get("/categories/{category_id}", response_model=Category, tags=["Categories"])
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(CategoryDB).filter(CategoryDB.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@app.get("/categories/name/{name}", response_model=Category, tags=["Categories"])
def read_category_by_name(name: str, db: Session = Depends(get_db)):
    db_category = db.query(CategoryDB).filter(CategoryDB.name == name).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


# Expense endpoints
@app.post("/expenses/", response_model=Expense, tags=["Expenses"])
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    # Check if category exists, if not create it
    db_category = db.query(CategoryDB).filter(CategoryDB.name == expense.category_name).first()
    if not db_category:
        db_category = CategoryDB(name=expense.category_name)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)

    # Create expense
    db_expense = ExpenseDB(
        amount=expense.amount,
        description=expense.description,
        date=expense.date,
        category_id=db_category.id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.get("/expenses/", response_model=List[ExpenseWithCategory], tags=["Expenses"])
def read_expenses(
        skip: int = 0,
        limit: int = 100,
        category_name: Optional[str] = None,
        db: Session = Depends(get_db)
):
    query = db.query(ExpenseDB)
    if category_name:
        query = query.join(CategoryDB).filter(CategoryDB.name == category_name)

    expenses = query.offset(skip).limit(limit).all()
    return expenses


@app.get("/expenses/{expense_id}", response_model=ExpenseWithCategory, tags=["Expenses"])
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense


@app.get("/expenses/totals/by-category", response_model=List[CategoryWithTotal], tags=["Reports"])
def get_expenses_by_category(db: Session = Depends(get_db)):
    results = (
        db.query(
            CategoryDB,
            func.sum(ExpenseDB.amount).label("total_expenses")
        )
        .join(ExpenseDB, CategoryDB.id == ExpenseDB.category_id)
        .group_by(CategoryDB.id)
        .all()
    )

    return [
        CategoryWithTotal(
            id=category.id,
            name=category.name,
            description=category.description,
            total_expenses=total or 0.0
        )
        for category, total in results
    ]


@app.get("/expenses/totals/since", tags=["Reports"])
def get_expenses_since(
        days: Optional[int] = None,
        start_date: Optional[datetime] = None,
        category_name: Optional[str] = None,
        db: Session = Depends(get_db)
):
    # Calculate the start date if days is provided
    if days is not None and start_date is None:
        start_date = datetime.now() - timedelta(days=days)
    elif start_date is None:
        # Default to last 30 days if neither is provided
        start_date = datetime.now() - timedelta(days=30)

    query = db.query(func.sum(ExpenseDB.amount).label("total"))

    # Apply date filter
    query = query.filter(ExpenseDB.date >= start_date)

    # Apply category filter if provided
    if category_name:
        query = query.join(CategoryDB).filter(CategoryDB.name == category_name)

    total = query.scalar() or 0.0

    return {
        "start_date": start_date,
        "category": category_name,
        "total_expenses": total
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8090)