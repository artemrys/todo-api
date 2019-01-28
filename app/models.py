from app import db


class TodoList(db.Document):
    name = db.StringField()

    def json(self):
        items = [
            item.json()
            for item in TodoItem.query.filter(TodoItem.todo_list.mongo_id == self.mongo_id).all()
        ]
        return {
            "mongo_id": str(self.mongo_id),
            "name": self.name,
            "items": items,
        }


class TodoItem(db.Document):
    text = db.StringField()
    todo_list = db.DocumentField(TodoList)
    due = db.DateTimeField()
    finished = db.BoolField()

    def json(self):
        return {
            "mongo_id": str(self.mongo_id),
            "list_mongo_id": str(self.todo_list.mongo_id),
            "text": self.text,
            "due": self.due,
            "finished": self.finished,
        }
