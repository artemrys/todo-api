### API for TODO app

It is a Flask application, storage is MongoDB.

[How to install MongoDB](https://docs.mongodb.com/manual/installation/)

API methods are available @ [Postman](https://www.getpostman.com/collections/e0c51461777178df4798)

#### Requirements

Could be installed using:

```bash
pipenv install .
```

#### Start

You can run this Flask application using (in `app` folder) (MacOS):

```bash
export MODE=dev; export FLASK_ENV=development; python run.py
```

#### Configuration

It is only about MongoDB storage, `DevelopmentConfig` is only available at the moment.
 But you can add other configurations like `TestingConfig`, `ProductionConfig` etc.

```python
    MONGOALCHEMY_DATABASE = "todo"
    MONGOALCHEMY_SERVER = "localhost"
    MONGOALCHEMY_PORT = 27017
    MONGOALCHEMY_USER = None
    MONGOALCHEMY_PASSWORD = None
```