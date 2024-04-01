from pydantic import BaseModel

class ToDo(BaseModel):
    name: str
    priority: int
    isDone: bool

class EditTodo(BaseModel):
    name: str
    priority: int