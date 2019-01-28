from datetime import datetime

from flask import request, jsonify
from werkzeug.exceptions import BadRequest

from app import app
from app.models import TodoList, TodoItem


@app.route("/api/v1/todo/lists", methods=["GET"])
def get_todo_lists():
    todo_lists = TodoList.query.all()
    result = []
    for todo_list in todo_lists:
        result.append(todo_list.json())
    return jsonify({
        "lists": result
    }), 200


@app.route("/api/v1/todo/lists/<list_mongo_id>", methods=["GET"])
def get_todo_list(list_mongo_id):
    todo_list = TodoList.query.get_or_404(list_mongo_id)
    return jsonify(todo_list.json()), 200


@app.route("/api/v1/todo/lists/<list_mongo_id>", methods=["PUT"])
def edit_todo_list(list_mongo_id):
    try:
        json = request.json
    except BadRequest:
        return jsonify({
            "error": "Empty json"
        }), 400
    name = json.get("name")
    if name is None:
        return jsonify({
            "error": "Name of todo-list could not be empty"
        }), 400
    todo_list = TodoList.query.get_or_404(list_mongo_id)
    todo_list.name = name
    todo_list.save()
    return jsonify(todo_list.json()), 200


@app.route("/api/v1/todo/lists", methods=["POST"])
def create_todo_list():
    try:
        json = request.json
    except BadRequest:
        return jsonify({
            "error": "Empty json"
        }), 400
    name = json.get("name")
    if name is None:
        return jsonify({
            "error": "Name of todo-list could not be empty"
        }), 400
    todo_list = TodoList(name=name)
    todo_list.save()
    return jsonify(todo_list.json()), 200


@app.route("/api/v1/todo/lists/<list_mongo_id>", methods=["DELETE"])
def delete_todo_list(list_mongo_id):
    todo_list = TodoList.query.get_or_404(list_mongo_id)
    todo_list.remove()
    items = TodoItem.query.filter(TodoItem.todo_list.mongo_id == list_mongo_id).all()
    for item in items:
        item.remove()
    return jsonify({"mongo_id": list_mongo_id}), 200


@app.route("/api/v1/todo/lists/<list_mongo_id>/items", methods=["POST"])
def create_todo_item(list_mongo_id):
    try:
        json = request.json
    except BadRequest:
        return jsonify({
            "error": "Empty json"
        }), 400

    text = json.get("text")
    if text is None:
        return jsonify({
            "error": "Text of todo-item could not be empty"
        }), 400

    due_raw = json.get("due")
    if due_raw is None:
        return jsonify({
            "error": "Due date of todo-item could not be empty"
        }), 400
    try:
        due = datetime.strptime(due_raw, "%Y/%m/%d")
    except ValueError:
        return jsonify({
            "error": "Cannot convert due to date object. Use format: %Y/%m/%d"
        }), 400

    finished = json.get("finished")
    if finished is None:
        return jsonify({
            "error": "Finished of todo-item could not be empty"
        }), 400

    todo_list = TodoList.query.get_or_404(list_mongo_id)
    todo_item = TodoItem(
        todo_list=todo_list,
        text=text,
        due=due,
        finished=finished,
    )
    todo_item.save()
    return jsonify(todo_item.json()), 200


@app.route("/api/v1/todo/lists/<list_mongo_id>/items/<item_mongo_id>", methods=["PUT"])
def edit_todo_item(list_mongo_id, item_mongo_id):
    try:
        json = request.json
    except BadRequest:
        return jsonify({
            "error": "Empty json"
        }), 400

    todo_list = TodoList.query.get(list_mongo_id)
    if todo_list is None:
        return jsonify({
            "error": f"No such todo-list with {list_mongo_id}",
        }), 404

    todo_item = TodoItem.query.get(item_mongo_id)
    if todo_item is None:
        return jsonify({
            "error": f"No such todo-item with {item_mongo_id}",
        }), 404

    text = json.get("text")
    if text is not None:
        todo_item.text = text

    due_raw = json.get("due")
    try:
        if due_raw is not None:
            due = datetime.strptime(due_raw, "%Y/%m/%d")
            todo_item.due = due
    except ValueError:
        return jsonify({
            "error": "Cannot convert due to date object. Use format: %Y/%m/%d"
        }), 400

    finished = json.get("finished")
    if finished is not None:
        todo_item.finished = finished

    todo_item.save()
    return jsonify(todo_item.json()), 200


@app.route("/api/v1/todo/lists/<list_mongo_id>/items/<item_mongo_id>", methods=["DELETE"])
def delete_todo_item(list_mongo_id, item_mongo_id):
    todo_list = TodoList.query.get(list_mongo_id)
    if todo_list is None:
        return jsonify({
            "error": f"No such todo-list with {list_mongo_id}",
        }), 404
    todo_item = TodoItem.query.get(item_mongo_id)
    if todo_item is None:
        return jsonify({
            "error": f"No such todo-item with {item_mongo_id}",
        }), 404
    todo_item.remove()
    return jsonify({"mongo_id": item_mongo_id})
