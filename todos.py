import json

import quart
from quart import Blueprint, request, Response, abort
from auth import assert_auth_header

todos_blueprint = Blueprint("todos", __name__)

_TODOS = {}

@todos_blueprint.post("/todos/<string:username>")
async def add_todo(username):
    assert_auth_header(request)
    request_data = await request.get_json(force=True)
    todo = request_data["todo"]
    todo_item = {"title": todo, "completed": False}
    if username not in _TODOS:
        _TODOS[username] = []
    _TODOS[username].append(todo_item)
    return Response(response='OK', status=200)

@todos_blueprint.get("/todos/<string:username>")
async def get_todos(username):
    assert_auth_header(request)
    completed = request.args.get('completed', None)
    todos = _TODOS.get(username, [])
    if completed is not None:
        completed = completed.lower() == 'true'
        todos = [todo for todo in todos if todo['completed'] == completed]
    return Response(response=json.dumps(todos), status=200)

@todos_blueprint.get("/todos/<string:username>/<int:todo_idx>")
async def get_single_todo(username, todo_idx):
    assert_auth_header(quart.request)
    todos = _TODOS.get(username, [])
    if 0 <= todo_idx < len(todos):
        return quart.Response(response=json.dumps(todos[todo_idx]), status=200)
    return quart.abort(404, "Todo not found")

@todos_blueprint.put("/todos/<string:username>/<int:todo_idx>")
async def update_todo(username, todo_idx):
    assert_auth_header(quart.request)
    request_data = await quart.request.get_json(force=True)
    new_title = request_data.get("title", None)
    todos = _TODOS.get(username, [])
    if 0 <= todo_idx < len(todos):
        if new_title:
            todos[todo_idx]["title"] = new_title
        return quart.Response(response='OK', status=200)
    return quart.abort(404, "Todo not found")


@todos_blueprint.patch("/todos/<string:username>/<int:todo_idx>/complete")
async def mark_todo_completed(username, todo_idx):
    assert_auth_header(quart.request)
    todos = _TODOS.get(username, [])
    if 0 <= todo_idx < len(todos):
        todos[todo_idx]["completed"] = True
        return quart.Response(response='OK', status=200)
    return quart.abort(404, "Todo not found")


@todos_blueprint.delete("/todos/<string:username>/<int:todo_idx>")
async def delete_todo(username, todo_idx):
    assert_auth_header(quart.request)
    todos = _TODOS.get(username, [])
    if 0 <= todo_idx < len(todos):
        todos.pop(todo_idx)
        return quart.Response(response='OK', status=200)
    return quart.abort(404, "Todo not found")
