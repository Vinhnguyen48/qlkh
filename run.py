from backend.app import main_web

# Khởi tạo ứng dụng Flask
app = main_web()

if __name__ == "__main__":
    app.run(debug=True)
