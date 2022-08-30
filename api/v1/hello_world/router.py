from fastapi.routing import APIRouter
from starlette import status
from .schemas import HelloWorldResponseSchema

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", status_code=status.HTTP_200_OK, response_model=HelloWorldResponseSchema)
def hello_world():
    return {"message": "Hello World"}
