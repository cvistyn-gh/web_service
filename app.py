import sys
import os

# Добавляем путь к папке flaskapp
sys.path.insert(0, '/home/cvistyn/web_service/flaskapp')

from some_app import app as application

if __name__ == "__main__":
    application.run()
