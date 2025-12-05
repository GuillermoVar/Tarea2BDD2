from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig
from app.models import Category

class CategoryReadDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig()

class CategoryCreateDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "created_at", "updated_at", "books"},
    )

class CategoryUpdateDTO(SQLAlchemyDTO[Category]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "created_at", "updated_at", "books"},
        partial=True,
    )
