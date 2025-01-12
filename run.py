from backend.app import main_web

flask_app = main_web()

if __name__== '__main__':
    flask_app.run(debug=True)