from flask import Flask, jsonify, abort, make_response, request
from models.TodosSQLite import todos

app = Flask(__name__)


@app.route('/api/v1/todos/', methods=['GET'])
def todos_list():
    return jsonify(todos.select_all())


@app.route('/api/v1/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = todos.select_where(todo_id)
    return jsonify(todo)


@app.route('/api/v1/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    result = todos.delete_where(todo_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route('/api/v1/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id, **kwargs):
    todo = todos.select_where(todo_id)[0]
    if not todo:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'done' in data and not isinstance(data.get('done'), int)
    ]):
        abort(400)

    if data['done'] < 0 or data['done'] > 1:
        abort(400)

    todo = {
        'title': data.get('title', todo[1]),
        'description': data.get('description', todo[2]),
        'done': data.get('done', todo[3])
    }
    todos.update(todo_id, **todo)
    return jsonify(todos.select_where(todo_id))


@app.route('/api/v1/todos/', methods=['POST'])
def create_todo():
    if not request.json:
        abort(400)

    if 'title' not in request.json:
        abort(400)

    todo = (
        request.json['title'],
        request.json.get('description', ""),
        0
    )
    todos.add_todo(todo)
    return jsonify(todos.select_all())


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status code': 404}))


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status code': 400}))
