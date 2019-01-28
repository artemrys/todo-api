import os

from app import create_app

if __name__ == '__main__':
    mode = os.getenv("MODE")
    app = create_app(mode)
    app.run()
