"""Controller for Book endpoints."""

from typing import Annotated, Sequence

from advanced_alchemy.exceptions import DuplicateKeyError, NotFoundError
from advanced_alchemy.filters import LimitOffset
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.exceptions import HTTPException
from litestar.params import Parameter

from app.controllers import duplicate_error_handler, not_found_error_handler
from app.dtos.book import BookCreateDTO, BookReadDTO, BookUpdateDTO
from app.models import Book, BookStats, Category
from app.repositories.book import BookRepository, provide_book_repo
from app.repositories.category import provide_category_repo, CategoryRepository


class BookController(Controller):
    """Controller for book management operations."""

    path = "/books"
    tags = ["books"]
    return_dto = BookReadDTO
    dependencies = {"books_repo": Provide(provide_book_repo), "categories_repo": Provide(provide_category_repo),
}
    exception_handlers = {
        NotFoundError: not_found_error_handler,
        DuplicateKeyError: duplicate_error_handler,
    }

    @get("/")
    async def list_books(self, books_repo: BookRepository) -> Sequence[Book]:
        """Get all books."""
        return books_repo.list()

    @get("/{id:int}")
    async def get_book(self, id: int, books_repo: BookRepository) -> Book:
        """Get a book by ID."""
        return books_repo.get(id)

    @post("/", dto=BookCreateDTO)
    async def create_book(
        self,
        data: DTOData[Book],
        books_repo: BookRepository,
    ) -> Book:
        
        valid_languages = {"es", "en", "fr", "de", "it", "pt"}

        language = data.as_builtins().get("language")

        if language not in valid_languages:
            raise HTTPException(
                status_code=400,
                detail="El idioma debe ser uno de: es, en, fr, de, it, pt."
            )
        
        # Validar stock > 0
        if data.as_builtins().get("stock", 1) <= 0:
            raise HTTPException(
                status_code=400,
                detail="El stock debe ser mayor a 0."
    )


        """Create a new book."""
        # Validar que el año esté entre 1000 y el año actual
        if not (1000 <= data.as_builtins()["published_year"] <= 2024):
            raise HTTPException(
                detail="El año de publicación debe estar entre 1000 y 2024",
                status_code=400,
            )
        return books_repo.add(data.create_instance())

    @patch("/{id:int}", dto=BookUpdateDTO)
    async def update_book(
        self,
        id: int,
        data: DTOData[Book],
        books_repo: BookRepository,
    ) -> Book:
        
        payload = data.as_builtins()

        # Validar stock >= 0 si viene en el body
        if "stock" in payload and payload["stock"] < 0:
            raise HTTPException(
                status_code=400,
                detail="El stock no puede ser negativo."
            )

        # Validar language en update también
        if "language" in payload:
            valid_languages = {"es", "en", "fr", "de", "it", "pt"}
            if payload["language"] not in valid_languages:
                raise HTTPException(
                    status_code=400,
                    detail="El idioma debe ser uno de: es, en, fr, de, it, pt."
                )


        """Update a book by ID."""
        book, _ = books_repo.get_and_update(match_fields="id", id=id, **data.as_builtins())

        return book

    @delete("/{id:int}")
    async def delete_book(self, id: int, books_repo: BookRepository) -> None:
        """Delete a book by ID."""
        books_repo.delete(id)

    @get("/search/")
    async def search_book_by_title(
        self,
        title: str,
        books_repo: BookRepository,
    ) -> Sequence[Book]:
        """Search books by title."""
        return books_repo.list(Book.title.ilike(f"%{title}%"))

    @get("/filter")
    async def filter_books_by_year(
        self,
        year_from: Annotated[int, Parameter(query="from")],
        to: int,
        books_repo: BookRepository,
    ) -> Sequence[Book]:
        """Filter books by published year."""
        return books_repo.list(Book.published_year.between(year_from, to))

    @get("/recent")
    async def get_recent_books(
        self,
        limit: Annotated[int, Parameter(query="limit", default=10, ge=1, le=50)],
        books_repo: BookRepository,
    ) -> Sequence[Book]:
        """Get most recent books."""
        return books_repo.list(
            LimitOffset(offset=0, limit=limit),
            order_by=Book.created_at.desc(),
        )

    @get("/stats")
    async def get_book_stats(
        self,
        books_repo: BookRepository,
    ) -> BookStats:
        """Get statistics about books."""
        total_books = books_repo.count()
        if total_books == 0:
            return BookStats(
                total_books=0,
                average_pages=0,
                oldest_publication_year=None,
                newest_publication_year=None,
            )

        books = books_repo.list()

        average_pages = sum(book.pages for book in books) / total_books
        oldest_year = min(book.published_year for book in books)
        newest_year = max(book.published_year for book in books)

        return BookStats(
            total_books=total_books,
            average_pages=average_pages,
            oldest_publication_year=oldest_year,
            newest_publication_year=newest_year,
        )
    
    @post("/{id:int}/assign-categories")
    async def assign_categories(
        self,
        id: int,
        category_ids: list[int],
        books_repo: BookRepository,
        categories_repo: CategoryRepository,
    ) -> Book:
        """Assign categories to a book."""
        # Obtener el libro
        book = books_repo.get(id)

        # Obtener las categorías existentes
        categories = categories_repo.list(Category.id.in_(category_ids))

        if len(categories) != len(category_ids):
            raise HTTPException(
                status_code=400,
                detail="Una o más categorías no existen."
            )

        # Asignar categorías
        book.categories = categories

        # Guardar cambios
        books_repo.update(book)

        return book

