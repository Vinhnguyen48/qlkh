from backend.app import main_web

app = main_web()

if __name__ == "__main__":
    app.run(debug=True)
