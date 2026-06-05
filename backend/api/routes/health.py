from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "voice-assisted-coding-agent",
    }
