from fastapi import APIRouter

router: APIRouter = APIRouter(
)

@router.get("/")
async def get_all_images(skip: int = 0, limit: int = 100):
    return {
        "message": "Hello World",
        "skip": skip,
        "limit": limit
    }

