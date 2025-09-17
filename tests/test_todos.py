from app.schemas.todo_schema import TodoOut
import pytest

prefix="/api/v1/todos/"

async def test_get_all_todos(authorized_client, test_todos):
    res = await authorized_client.get(prefix)
    
    todos = [TodoOut(**todo) for todo in res.json()]
    assert len(todos) == len(test_todos)
    assert res.status_code == 200


async def test_unauthorized_user_get_all_todos(client, test_todos):
    res = await client.get(prefix)
    assert res.json() == {"detail": "Not authenticated"}
    assert res.status_code == 401
    
    
async def test_unauthorized_user_get_todo_by_id(client, test_todos):
    res = await client.get(f"{prefix}1")
    assert res.json() == {"detail": "Not authenticated"}
    assert res.status_code == 401
    
    
async def test_get_todo_by_id(authorized_client, test_todos):
    res = await authorized_client.get(f"{prefix}1")
    TodoOut(**res.json())
    assert res.status_code == 200
    
    
async def test_get_todo_by_id_which_not_exist(authorized_client, test_todos):
    res = await authorized_client.get(f"{prefix}999")
    assert res.json() == {
        "message": "Todo not found",
        "error_code": "todo_not_found",
        "detail": "Todo not found"
    }
    assert res.status_code == 404





@pytest.mark.parametrize("title, description, priority, complete", [
    ("Learning React", "it is gonna be long huh??", 3, False),
    ("Learning", "it is gonna be good", 5, True),
])
async def test_create_todo(test_user, authorized_client, test_todos, title, description, priority, complete):
    todo_data = { 
            "title": title,
            "description": description,
            "priority": priority,
            "complete": complete
        }

    res = await authorized_client.post(prefix, json=todo_data)
    created_todo = TodoOut(**res.json())
    assert created_todo.title == title
    assert created_todo.description == description
    assert created_todo.priority == priority
    assert created_todo.complete == complete
    assert res.status_code == 201




async def test_unathorized_user_create_todo(test_user, client):
    todo_data = { 
            "title": "title",
            "description": "description",
            "priority": 1,
            "complete": False
        }

    res = await client.post(prefix, json=todo_data)
    assert res.json() == {"detail": "Not authenticated"}
    assert res.status_code == 401




async def test_unathorized_user_delete_todo(test_user, client, test_todos):
    res = await client.delete(f"{prefix}1")
    assert res.json() == {"detail": "Not authenticated"}
    assert res.status_code == 401


async def test_delete_todo(test_user, authorized_client, test_todos):
    res = await authorized_client.delete(f"{prefix}1")
    assert res.status_code == 204
    
    
async def test_delete_todo_which_not_exist(test_user, authorized_client, test_todos):
    res = await authorized_client.delete(f"{prefix}999")
    assert res.json() == {
    "message": "Todo not found",
    "error_code": "todo_not_found",
    "detail": "Todo not found"
}
    assert res.status_code == 404
    
    
    


@pytest.mark.parametrize("title, description, priority, complete, todo_id", [
    ("Learning React!", "it is gonna be long huh???", 2, False, 1),
    (None, None, 5, False, 2),
])
async def test_update_todo(test_user, authorized_client, test_todos, title, description, priority, complete, todo_id):
    todo_data = { 
            "title": title,
            "description": description,
            "priority": priority,
            "complete": complete
        }

    res = await authorized_client.patch(f"{prefix}{todo_id}", json=todo_data)
    updated_todo = TodoOut(**res.json())
    assert updated_todo.priority == priority
    assert res.status_code == 200



    
async def test_unathorized_user_update_todo(test_user, client, test_todos):
    todo_data = { 
            "priority": 1
        }
    res = await client.patch(f"{prefix}1", json=todo_data)
    assert res.json() == {"detail": "Not authenticated"}
    assert res.status_code == 401


async def test_update_todo_which_not_exist(test_user, authorized_client, test_todos):
    todo_data = { 
            "priority": 1
        }
    res = await authorized_client.patch(f"{prefix}999", json=todo_data)
    assert res.json() == {
    "message": "Todo not found",
    "error_code": "todo_not_found",
    "detail": "Todo not found"
}
    assert res.status_code == 404