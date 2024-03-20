from fastapi import APIRouter, Request

router = APIRouter(
    tags=["bookmarks", "feed"]
)


@router.get("/all")
async def get_all(request: Request, sort_by: str = None, asc: bool = True):
    if sort_by == None:
        sort_by = 'timestamp'
    