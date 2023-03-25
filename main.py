import json

import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

_SERVICE_AUTH_KEY = "TEST"
_TODOS = {}


def assert_auth_header(req):
    assert req.headers.get(
        "Authorization", None) == f"Bearer {_SERVICE_AUTH_KEY}"


@app.post("/todos/<string:username>")
async def add_todo(username):
    assert_auth_header(quart.request)
    request_data = await quart.request.get_json(force=True)
    todo = request_data["todo"]
    todo_item = {"title": todo, "completed": False}
    if username not in _TODOS:
        _TODOS[username] = []
    _TODOS[username].append(todo_item)
    return quart.Response(response='OK', status=200)


@app.get("/todos/<string:username>")
async def get_todos(username):
    assert_auth_header(quart.request)
    completed = request.args.get('completed', None)
    todos = _TODOS.get(username, [])
    if completed is not None:
        completed = completed.lower() == 'true'
        todos = [todo for todo in todos if todo['completed'] == completed]
    return quart.Response(response=json.dumps(todos), status=200)


@app.get("/todos/<string:username>/<int:todo_idx>")
async def get_single_todo(username, todo_idx):
    assert_auth_header(quart.request)
    todos = _TODOS.get(username, [])
    if 0 <= todo_idx < len(todos):
        return quart.Response(response=json.dumps(todos[todo_idx]), status=200)
    return quart.abort(404, "Todo not found")

@app.put("/todos/<string:username>/<int:todo_idx>")
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


@app.patch("/todos/<string:username>/<int:todo_idx>/complete")
async def mark_todo_completed(username, todo_idx):
    assert_auth_header(quart.request)
    todos = _TODOS.get(username, [])
    if 0 <= todo_idx < len(todos):
        todos[todo_idx]["completed"] = True
        return quart.Response(response='OK', status=200)
    return quart.abort(404, "Todo not found")


@app.delete("/todos/<string:username>/<int:todo_idx>")
async def delete_todo(username, todo_idx):
    assert_auth_header(quart.request)
    todos = _TODOS.get(username, [])
    if 0 <= todo_idx < len(todos):
        todos.pop(todo_idx)
        return quart.Response(response='OK', status=200)
    return quart.abort(404, "Todo not found")


@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("manifest.json") as f:
        text = f.read()
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/yaml")


def main():
    app.run(debug=True, host="0.0.0.0", port=5002)


if __name__ == "__main__":
    main()