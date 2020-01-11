from flask import Flask, render_template, request, jsonify
from script import run, returnIssues

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
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
            # if not "tokens" in request.json:
            #     return jsonify({
            #         "error": "É necessário que seja informada no body uma lista de tokens para correta execução da ferramenta!"
            #     })

            owner = request.json["owner"]
            repository = request.json["repository"]
            # tokens = request.json["tokens"]
            run(owner, repository)
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"error": str(e)})


@app.route('/issues', methods=["GET"])
def get_issues():
    if request.method == "GET":
        try:
            if not "owner" in request.json:
                return jsonify({
                    "error":
                    "É necessário que seja informado no body o dono do repositório a ser recuperado!"
                })
            if not "repository" in request.json:
                return jsonify({
                    "error":
                    "É necessário que seja informado no body o nome do repositório a ser recuperado!"
                })

            owner = request.json["owner"]
            repository = request.json["repository"]
            limit = request.json["limit"] if "limit" in request.json else None

            issues = returnIssues(owner, repository, limit)
            return jsonify(issues)
        except Exception as e:
            return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=5000)
