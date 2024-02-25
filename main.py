from fastapi import FastAPI
from models import Todo

app = FastAPI()

@app.get("/")
async def read_root():
    return {"page": "Hello World"}

todos = list()

# Get all todo
@app.get("/todos")
async def get_todos():
    return {"todos": todos}

# Get single todo
@app.get("/todos/{todo_id}")
async def get_single_todo(todo_id: int):
    for todo in todos:
        if todo.id==todo_id:
            return todo
    return {"message": f"No Todos found for id {todo_id}"}

# Create a todo
@app.post("/todos")
async def create_todos(todo: Todo):
    todos.append(todo)
    return {"message": "Todo Added"}

# Update a todo
@app.put("/todos/{todo_id}")
async def update_todos(todo_id: int, todo_object: Todo):
    for todo in todos:
        if todo.id==todo_id:
            todo.id = todo_id
            todo.item = todo_object.item
            return todo
    return {"message": f"No Todos found for id {todo_id} to update"}


# Delete a tod
@app.delete("/todos/{todo_id}")
async def delete_todos(todo_id: int):
    for todo in todos:
        if todo.id==todo_id:
            todos.remove(todo)
            return {"message": f"Todos with id {todo_id} deleted"}
    return {"message": f"No Todos found for id {todo_id}"}
