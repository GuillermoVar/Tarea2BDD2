from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy.orm import Session
from app.models import Category

class CategoryRepository(SQLAlchemySyncRepository[Category]):
    model_type = Category

async def provide_category_repo(db_session: Session) -> CategoryRepository:
    return CategoryRepository(session=db_session, auto_commit=True)
