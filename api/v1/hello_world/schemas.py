from pydantic.main import BaseModel


class HelloWorldResponseSchema(BaseModel):
    message: str = "Hello World"
