from fastapi import APIRouter, Request

router = APIRouter(tags=["debug", "sentry"])

@router.get("/test-sentry")
async def tets_sentry(request: Request):
    raise Exception("Test Sentry")
