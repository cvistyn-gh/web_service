# from some_app import app

# if __name__ == "__main__":
    # app.run()
import sys
path = '/home/cvistyn/web_service'
if path not in sys.path:
    sys.path.append(path)

from flaskapp.some_app import app as application
