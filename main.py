from quart import Quart
from quart_cors import cors

from todos import todos_blueprint
from plugins import plugins_blueprint

app = Quart(__name__)
app = cors(app, allow_origin="https://chat.openai.com")

app.register_blueprint(todos_blueprint)
app.register_blueprint(plugins_blueprint)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)