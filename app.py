from flask import *


app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('home.html')