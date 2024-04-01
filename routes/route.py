import json
from fastapi import APIRouter, Response, status
from ..models.todos import EditTodo, ToDo
from ..config.database import todo_collection
from ..schema.schemas import list_serial
from ..utils.utils import validate_model, InvalidPriorityException, InvalidToDoNameException
from bson import ObjectId

router = APIRouter()

#GET ALL ToDoS

@router.get("/todos/")
async def get_todos(response: Response, completness="all", searchString="", order="none" ):

    try:
        todos = todo_collection.find()

        if order != "none":
            if order == "asc":
                todos = todos.sort("priority", -1)
            elif order == "desc":
                todos = todos.sort("priority", 1)
            else:
                raise Exception("wrong order query parameter!")

        if completness != "all":
            if completness == "done":
                todos = filter(lambda x: x["isDone"] == True, todos)
            elif completness == "undone":
                todos = filter(lambda x: x["isDone"] == False, todos)
            else:
                raise Exception("wrong completness query parameter!")

        if searchString != "":
            todos = filter(lambda x: searchString.lower().replace(" ", "") in x["name"].lower().replace(" ", ""), todos)
            
        response.status_code = status.HTTP_200_OK
        return list_serial(todos)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return f"Couldn't get the todos list: "

#POST A NEW ToDo

@router.post("/todos/")
async def post_todo(todo: ToDo, response: Response) :
    try:
        await validate_model(todo)
        todo_collection.insert_one(dict(todo))
        response.status_code = status.HTTP_201_CREATED
        return "Successfully created new todo item!"
    except InvalidPriorityException as e:
        response.status_code = status.HTTP_403_FORBIDDEN
        return f"Couldn't create new todo item: {str(e)}"
    except InvalidToDoNameException as e:
        response.status_code = status.HTTP_403_FORBIDDEN
        return f"Couldn't create new todo item: {str(e)}"
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return "Couldn't create new todo item, try again later."


#PUT NEW INFO INTO AN EXISTING ToDo
    
@router.put("/todos/{id}")
async def edit_todo(id: str, todo: EditTodo, response: Response):
    try:
        await validate_model(todo)
        todo_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(todo)})
        response.status_code = status.HTTP_200_OK
        return "Successfully updated the todo item!"
    except InvalidPriorityException as e:
        response.status_code = status.HTTP_403_FORBIDDEN
        return f"Couldn't update the todo item: {str(e)}"
    except InvalidToDoNameException as e:
        response.status_code = status.HTTP_403_FORBIDDEN
        return f"Couldn't update the todo item: {str(e)}"
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return "Couldn't update the todo item, try again later."

#GET NEW COMPLETENESS FOR THE ToDo
    
@router.get("/todos/switch-completeness/{id}")
async def switch_completeness(id: str, response: Response):
    try: 
        todo_collection.find_one_and_update({"_id": ObjectId(id)}, [{"$set": {"isDone": {"$not": "$isDone"}}}])
        response.status_code = status.HTTP_200_OK
        return "Successfully updated completeness status for the todo item!"
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return "Couldn't update the todo item, try again later."

#DELETE AN EXISTING ToDo
    
@router.delete("/todos/{id}")
async def delete_todo(id: str, response: Response):
    try:
        todo_collection.find_one_and_delete({"_id": ObjectId(id)})
        response.status_code = status.HTTP_200_OK
        return "Successfully deleted the todo item!"
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return "Couldn't delete the todo item, try again later."
