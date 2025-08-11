from sqlalchemy import Column, Integer, String, Float, ForeignKey, func, DateTime
from sqlalchemy.orm import relationship
from db.base_class import Base
from datetime import datetime

class CategoryDB(Base):
  __tablename__ = "categories"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(255), unique=True, index=True)
  description = Column(String(500), nullable=True)

  expenses = relationship("ExpenseDB", back_populates="category")


class ExpenseDB(Base):
  __tablename__ = "expenses"

  id = Column(Integer, primary_key=True, index=True)
  amount = Column(Float)
  description = Column(String(500), nullable=True)
  date = Column(DateTime, default=datetime.now)
  category_id = Column(Integer, ForeignKey("categories.id"))

  category = relationship("CategoryDB", back_populates="expenses")