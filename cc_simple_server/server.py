from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from cc_simple_server.models import TaskCreate
from cc_simple_server.models import TaskRead
from cc_simple_server.database import init_db
from cc_simple_server.database import get_db_connection

# init
init_db()

app = FastAPI()

############################################
# Edit the code below this line
############################################


@app.get("/")
async def read_root():
    """
    This is already working!!!! Welcome to the Cloud Computing!
    """
    return {"message": "Welcome to the Cloud Computing!"}


# POST ROUTE data is sent in the body of the request
@app.post("/tasks/", response_model=TaskRead)
async def create_task(task_data: TaskCreate):
    """
    Create a new task

    Args:
        task_data (TaskCreate): The task data to be created

    Returns:
        TaskRead: The created task data
    """
    try:
        conn = get_db_connection()
        init_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, description, completed)
                       VALUES (?, ?, ?)
''', (task_data.title, task_data.description, task_data.completed))
    except:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_ERROR, detail = "Database connection failed")
    finally:
        conn.commit()
        print("New task successfully added")
        conn.close()
    
    return task_data

# GET ROUTE to get all tasks
@app.get("/tasks/", response_model=list[TaskRead])
async def get_tasks():
    """
    Get all tasks in the whole wide database

    Args:
        None

    Returns:
        list[TaskRead]: A list of all tasks in the database
    """
    try:
        conn = get_db_connection()
        init_db()
        cursor = conn.cursor()
        all_tasks = cursor.fetchall()
    except:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_ERROR, detail = "Database connection failed")
    finally:
        conn.commit()
        conn.close()
        return all_tasks


# UPDATE ROUTE data is sent in the body of the request and the task_id is in the URL
@app.put("/tasks/{task_id}/", response_model=TaskRead)
async def update_task(task_id: int, task_data: TaskCreate):
    """
    Update a task by its ID

    Args:
        task_id (int): The ID of the task to be updated
        task_data (TaskCreate): The task data to be updated

    Returns:
        TaskRead: The updated task data
    """
    try:
        conn = get_db_connection()
        init_db()
        cursor = conn.cursor()
        cursor.execute('''
                       UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?''', (task_data.title, task_data.description, task_data.completed, task_id))
    except:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_ERROR, detail = "Database connection failed")
    finally:
        conn.commit()
        print(f"task {task_id} successfully updated")
        conn.close()


# DELETE ROUTE task_id is in the URL
@app.delete("/tasks/{task_id}/")
async def delete_task(task_id: int):
    """
    Delete a task by its ID

    Args:
        task_id (int): The ID of the task to be deleted

    Returns:
        dict: A message indicating that the task was deleted successfully
    """
    try:
        conn = get_db_connection()
        init_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    except:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_ERROR, detail = "Database connection failed")
    finally:
        conn.commit()
        print(f"task {task_id} successfully deleted")
        conn.close()
