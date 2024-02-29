from fastapi import APIRouter
from controllers.movies_controllers import router as movie_router

router = APIRouter()
router.include_router(movie_router)