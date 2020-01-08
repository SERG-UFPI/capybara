from flask import *

app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template('home.html')


# Insert new repository to database
@app.route('/insert', methods=["POST"])
def insert_repository():
    if request.method == "POST":
        try:
            if not "owner" in request.json:
                return jsonify({
                    "error":
                    "É necessário que seja informado no body o dono do repositório a ser inserido!"
                })
            if not "repository" in request.json:
                return jsonify({
                    "error":
                    "É necessário que seja informado no body o nome do repositório a ser inserido!"
                })

            owner = request.json["owner"]
            repository = request.json["repository"]
            run(owner, repository)
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"error": e})
