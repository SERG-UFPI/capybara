from flask import *
from script import run

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=5000)
