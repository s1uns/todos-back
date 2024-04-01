from ..models.todos import ToDo

async def validate_model(model: ToDo):


    if len(model.name) < 5 or len(model.name) > 50:
        raise InvalidToDoNameException("the title of the task should be between 5 and 50 characters long.")
    
    if model.priority < 1 or  model.priority > 10:
        raise InvalidPriorityException("the priority of a task must be in the range from 1 to 10.")

class InvalidToDoNameException(Exception):
    pass

class InvalidPriorityException(Exception):
    pass