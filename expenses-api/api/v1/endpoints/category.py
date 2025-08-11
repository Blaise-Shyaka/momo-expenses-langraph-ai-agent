from fastapi import APIRouter, HTTPException, Depends
from schemas.schema import Category, CategoryCreate
from db.models import CategoryDB
from sqlalchemy.orm import Session
from typing import List
from api.deps import get_db
from sqlalchemy import select, func

router = APIRouter()

@router.post("/", response_model=Category, tags=["Categories"])
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    category_stmt = select(CategoryDB).where(func.lower(CategoryDB.name) == category.name.lower())
    result = await db.execute(category_stmt)
    category_exists = result.scalars().first()
    if category_exists:
        raise HTTPException(status_code=400, detail="Category already exists")

    db_category = CategoryDB(**category.model_dump())
    await db.add(db_category)
    await db.commit()
    return db_category


@router.get("/", response_model=List[Category], tags=["Categories"])
async def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    #  TODO: Try to handle pagination in a much better way
    categories_stmt = select(CategoryDB).offset(skip).limit(limit)
    result = await db.execute(categories_stmt)
    return result.scalars().all()

@router.get("/{category_id}", response_model=Category, tags=["Categories"])
async def read_category(category_id: int, db: Session = Depends(get_db)):
    category_stmt = select(CategoryDB).where(CategoryDB.id == category_id)
    db_category = await db.execute(category_stmt).scalars().first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.get("/name/{name}", response_model=Category, tags=["Categories"])
async def read_category_by_name(name: str, db: Session = Depends(get_db)):
    category_stmt = select(CategoryDB).where(func.lower(CategoryDB.name) == name.lower())
    db_category = await db.execute(category_stmt).scalars().first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category
