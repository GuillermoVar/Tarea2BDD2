from advanced_alchemy.extensions.litestar import SQLAlchemyDTO, SQLAlchemyDTOConfig
from app.models import Review

class ReviewReadDTO(SQLAlchemyDTO[Review]):
    
    config = SQLAlchemyDTOConfig(
        include={"user", "book"}
    )

class ReviewCreateDTO(SQLAlchemyDTO[Review]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "created_at", "updated_at", "user", "book"}
    )

class ReviewUpdateDTO(SQLAlchemyDTO[Review]):
    config = SQLAlchemyDTOConfig(
        exclude={"id", "created_at", "updated_at", "user", "book"},
        partial=True,
    )
