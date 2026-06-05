from fastapi import APIRouter

router = APIRouter(
    prefix="/agent",
    tags=["agent"],
)


@router.post("/query")
def query_agent():

    return {"message": ("Agent endpoint not implemented yet")}
