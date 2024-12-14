from fastapi import APIRouter
from v1.endpoints.autor_endpoint import router as author_router
from v1.endpoints.readers_endpoint import router as reader_router
from v1.endpoints.books_endpoint import router as book_router
from v1.endpoints.borrows_endpoint import router as borrow_router

api_router = APIRouter()
api_router.include_router(author_router, prefix="/authors", tags=["Authors"])
api_router.include_router(reader_router, prefix="/readers", tags=["Readers"])
api_router.include_router(book_router, prefix="/books", tags=["Book"])
api_router.include_router(borrow_router, prefix="/borrows", tags=["Borrows"])
