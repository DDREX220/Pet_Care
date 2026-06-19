<<<<<<< HEAD
from app import create_app
app = create_app()
=======
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World! This is my first Flask website."
>>>>>>> 4ef31d859b8712b198bfb64d02ce9eb1a9cc1829

if __name__ == "__main__":
        app.run(debug=True)
        
        
        